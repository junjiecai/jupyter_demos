class DataExplore:
    def __init__(self, df):
        self.df = df
        self.configs = self.set_default_configs(df)

    def set_filter(self):
        pass

    def update_config(self, configs):
        self.configs._update(configs)

    def indivisual_analyse(self):
        pass

    def visualize_indivisual_analyze(self, output):
        pass

    def pairwise_analyse(self, features):
        pass

    def visualize_parise_analyze(self, output):
        pass


def auto_config(df):
    return {}


config = auto_config(df)

config.update(custom_config)


def features_analysis(df, config):
    return None


def visualize_analysis(results):
    pass


results = features_analysis(df, config)

visualize_analysis(results)


def pairwise_analysis(df, config):
    return None


def visualize_pairwise_analysis(results):
    pass


pairwise_results = pairwise_analysis(df, config)
visualize_pairwise_analysis(pairwise_results)
