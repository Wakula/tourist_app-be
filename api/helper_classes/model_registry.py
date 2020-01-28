class ModelRegistry:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ModelRegistry, cls).__new__(cls)
        return cls.instance

    def set_app_models(self, model_list):

        for model in model_list:
            setattr(self, model.__name__, model)
