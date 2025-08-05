// Secure TLS channel code using OpenSSL libssl - vulnerabilities fixed
// This is an example showing how to address the security issues found

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/x509v3.h>

// Initialize OpenSSL library (simplified for modern OpenSSL)
void init_openssl() {
    // These functions are no-ops in OpenSSL 1.1.0+ and can be omitted
    // SSL_library_init() is called automatically
}

// Cleanup OpenSSL library (simplified for modern OpenSSL)
void cleanup_openssl() {
    // EVP_cleanup() is deprecated and unnecessary in modern OpenSSL
}

// Create SSL context with security configurations
SSL_CTX *create_context(int is_server) {
    const SSL_METHOD *method;
    SSL_CTX *ctx;
    
    if (is_server)
        method = TLS_server_method();
    else
        method = TLS_client_method();
    
    ctx = SSL_CTX_new(method);
    if (!ctx) {
        fprintf(stderr, "Unable to create SSL context\n");
        ERR_print_errors_fp(stderr);
        return NULL;
    }
    
    // SECURITY FIX: Disable weak protocols and configure secure options
    SSL_CTX_set_options(ctx, 
        SSL_OP_NO_SSLv2 | SSL_OP_NO_SSLv3 | 
        SSL_OP_NO_TLSv1 | SSL_OP_NO_TLSv1_1 |
        SSL_OP_NO_COMPRESSION |
        SSL_OP_CIPHER_SERVER_PREFERENCE);
    
    // SECURITY FIX: Set secure cipher list (prefer AEAD ciphers with forward secrecy)
    if (SSL_CTX_set_cipher_list(ctx, 
        "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS:!RC4") != 1) {
        fprintf(stderr, "Failed to set cipher list\n");
        SSL_CTX_free(ctx);
        return NULL;
    }
    
    // SECURITY FIX: Set minimum TLS version to 1.2
    if (SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION) != 1) {
        fprintf(stderr, "Failed to set minimum TLS version\n");
        SSL_CTX_free(ctx);
        return NULL;
    }
    
    return ctx;
}

// Configure server context with cert and key (with validation)
int configure_server_context(SSL_CTX *ctx, const char *cert_file, const char *key_file) {
    if (!ctx || !cert_file || !key_file) {
        fprintf(stderr, "Invalid parameters\n");
        return 0;
    }
    
    if (SSL_CTX_use_certificate_file(ctx, cert_file, SSL_FILETYPE_PEM) <= 0) {
        fprintf(stderr, "Failed to load certificate file\n");
        ERR_print_errors_fp(stderr);
        return 0;
    }
    
    if (SSL_CTX_use_PrivateKey_file(ctx, key_file, SSL_FILETYPE_PEM) <= 0) {
        fprintf(stderr, "Failed to load private key file\n");
        ERR_print_errors_fp(stderr);
        return 0;
    }
    
    // SECURITY FIX: Verify that private key matches certificate
    if (!SSL_CTX_check_private_key(ctx)) {
        fprintf(stderr, "Private key does not match certificate\n");
        return 0;
    }
    
    return 1;
}

// SECURITY FIX: Secure hostname resolution using getaddrinfo
int resolve_hostname(const char *hostname, const char *port, struct addrinfo **result) {
    struct addrinfo hints;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;    // Allow IPv4 or IPv6
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_ADDRCONFIG;
    
    int status = getaddrinfo(hostname, port, &hints, result);
    if (status != 0) {
        fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(status));
        return 0;
    }
    return 1;
}

// Connect to server with TLS (client) - SECURITY FIXED VERSION
SSL *tls_connect(const char *hostname, int port, SSL_CTX *ctx) {
    if (!hostname || !ctx || port <= 0 || port > 65535) {
        fprintf(stderr, "Invalid parameters\n");
        return NULL;
    }
    
    struct addrinfo *result, *rp;
    char port_str[16];
    snprintf(port_str, sizeof(port_str), "%d", port);
    
    // SECURITY FIX: Use secure DNS resolution
    if (!resolve_hostname(hostname, port_str, &result)) {
        return NULL;
    }
    
    int sock = -1;
    // Try each address until we successfully connect
    for (rp = result; rp != NULL; rp = rp->ai_next) {
        sock = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);
        if (sock == -1) continue;
        
        if (connect(sock, rp->ai_addr, rp->ai_addrlen) != -1) {
            break; // Success
        }
        close(sock);
        sock = -1;
    }
    
    freeaddrinfo(result);
    
    if (sock == -1) {
        fprintf(stderr, "Failed to connect to %s:%d\n", hostname, port);
        return NULL;
    }
    
    SSL *ssl = SSL_new(ctx);
    if (!ssl) {
        close(sock);
        return NULL;
    }
    
    // SECURITY FIX: Enable certificate verification
    SSL_set_verify(ssl, SSL_VERIFY_PEER, NULL);
    
    // SECURITY FIX: Enable hostname verification
    if (SSL_set1_host(ssl, hostname) != 1) {
        fprintf(stderr, "Failed to set hostname for verification\n");
        SSL_free(ssl);
        close(sock);
        return NULL;
    }
    
    SSL_set_fd(ssl, sock);
    
    if (SSL_connect(ssl) <= 0) {
        fprintf(stderr, "SSL connection failed\n");
        ERR_print_errors_fp(stderr);
        SSL_free(ssl);
        close(sock);
        return NULL;
    }
    
    // Verify the certificate was validated
    long verify_result = SSL_get_verify_result(ssl);
    if (verify_result != X509_V_OK) {
        fprintf(stderr, "Certificate verification failed: %ld\n", verify_result);
        SSL_free(ssl);
        close(sock);
        return NULL;
    }
    
    return ssl;
}

// Setup TLS server socket (with security fixes)
int tls_server_listen(int port) {
    if (port <= 0 || port > 65535) {
        fprintf(stderr, "Invalid port number\n");
        return -1;
    }
    
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("Unable to create socket");
        return -1;
    }
    
    // SECURITY FIX: Enable address reuse
    int opt = 1;
    if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("setsockopt SO_REUSEADDR failed");
        close(sockfd);
        return -1;
    }
    
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = INADDR_ANY;
    
    if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("Unable to bind");
        close(sockfd);
        return -1;
    }
    
    // SECURITY FIX: Use reasonable backlog instead of 1
    if (listen(sockfd, 128) < 0) {
        perror("Unable to listen");
        close(sockfd);
        return -1;
    }
    
    return sockfd;
}

// Accept a TLS connection (server) - FIXED VERSION
SSL *tls_accept(int server_sock, SSL_CTX *ctx) {
    if (server_sock < 0 || !ctx) {
        fprintf(stderr, "Invalid parameters\n");
        return NULL;
    }
    
    struct sockaddr_in addr;
    socklen_t len = sizeof(addr);  // SECURITY FIX: Use correct type
    
    int client_sock = accept(server_sock, (struct sockaddr*)&addr, &len);
    if (client_sock < 0) {
        perror("Unable to accept");
        return NULL;
    }
    
    SSL *ssl = SSL_new(ctx);
    if (!ssl) {
        close(client_sock);
        return NULL;
    }
    
    SSL_set_fd(ssl, client_sock);
    
    if (SSL_accept(ssl) <= 0) {
        fprintf(stderr, "SSL accept failed\n");
        ERR_print_errors_fp(stderr);
        SSL_free(ssl);
        close(client_sock);
        return NULL;
    }
    
    return ssl;
}

// Send data over TLS with proper error handling
int tls_send(SSL *ssl, const void *buf, int len) {
    if (!ssl || !buf || len <= 0) {
        return -1;
    }
    
    int bytes_sent = 0;
    while (bytes_sent < len) {
        int ret = SSL_write(ssl, (char*)buf + bytes_sent, len - bytes_sent);
        if (ret <= 0) {
            int error = SSL_get_error(ssl, ret);
            if (error == SSL_ERROR_WANT_WRITE || error == SSL_ERROR_WANT_READ) {
                continue; // Retry
            }
            return -1; // Real error
        }
        bytes_sent += ret;
    }
    return bytes_sent;
}

// Receive data over TLS with proper error handling
int tls_recv(SSL *ssl, void *buf, int len) {
    if (!ssl || !buf || len <= 0) {
        return -1;
    }
    
    int ret = SSL_read(ssl, buf, len);
    if (ret <= 0) {
        int error = SSL_get_error(ssl, ret);
        if (error == SSL_ERROR_WANT_READ || error == SSL_ERROR_WANT_WRITE) {
            return 0; // Would block, try again later
        }
        return -1; // Real error
    }
    return ret;
}

// Close TLS connection with proper shutdown
void tls_close(SSL *ssl) {
    if (!ssl) return;
    
    int sock = SSL_get_fd(ssl);
    
    // Attempt clean SSL shutdown
    int shutdown_ret = SSL_shutdown(ssl);
    if (shutdown_ret == 0) {
        // First call returned 0, call again for bidirectional shutdown
        SSL_shutdown(ssl);
    }
    
    SSL_free(ssl);
    if (sock >= 0) {
        close(sock);
    }
}