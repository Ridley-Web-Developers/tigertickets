class Config:
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_DEBUG = 0
    MAIL_USE_TLS = True
    MAIL_PORT = 587
    MAIL_USERNAME = 'mand_tickets@ridleycollege.com'
    MAIL_PASSWORD = 'Student2019!'
    MAIL_DEFAULT_SENDER = 'mand_tickets@ridleycollege.com'
    MONGO_URI = 'mongodb+srv://tigers:Student!@tiger-tickets-n3wt7.mongodb.net/tigertickets?retryWrites=true&w=majority'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
