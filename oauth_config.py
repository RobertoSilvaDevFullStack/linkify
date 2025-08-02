"""
Configuração OAuth2 para integração com provedores sociais
"""

import os
from authlib.integrations.starlette_client import OAuth

# Configurações OAuth2 dos provedores
OAUTH_CONFIG = {
    'google': {
        'client_id': os.getenv('GOOGLE_CLIENT_ID', 'seu-google-client-id'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET', 'seu-google-client-secret'),
        'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration',
        'client_kwargs': {
            'scope': 'openid email profile'
        }
    },
    'github': {
        'client_id': os.getenv('GITHUB_CLIENT_ID', 'seu-github-client-id'),
        'client_secret': os.getenv('GITHUB_CLIENT_SECRET', 'seu-github-client-secret'),
        'access_token_url': 'https://github.com/login/oauth/access_token',
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'api_base_url': 'https://api.github.com/',
        'client_kwargs': {
            'scope': 'user:email'
        }
    },
    'microsoft': {
        'client_id': os.getenv('MICROSOFT_CLIENT_ID', 'seu-microsoft-client-id'),
        'client_secret': os.getenv('MICROSOFT_CLIENT_SECRET', 'seu-microsoft-client-secret'),
        'server_metadata_url': 'https://login.microsoftonline.com/common/v2.0/.well-known/openid_configuration',
        'client_kwargs': {
            'scope': 'openid email profile'
        }
    },
    'apple': {
        'client_id': os.getenv('APPLE_CLIENT_ID', 'seu-apple-client-id'),
        'client_secret': os.getenv('APPLE_CLIENT_SECRET', 'seu-apple-client-secret'),
        'server_metadata_url': 'https://appleid.apple.com/.well-known/openid_configuration',
        'client_kwargs': {
            'scope': 'openid email name'
        }
    }
}

def setup_oauth(app):
    """Configura OAuth2 para a aplicação"""
    oauth = OAuth()
    
    # Configurar cada provedor OAuth
    for provider, config in OAUTH_CONFIG.items():
        oauth.register(
            name=provider,
            **config
        )
    
    # Para Starlette/FastAPI, não precisamos do init_app
    return oauth
