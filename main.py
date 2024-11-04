from my_find_update_plugin.my_find_update_plugin import MyFindUpdatePlugin
from jmcomic import create_option, JmModuleConfig

JmModuleConfig.register_plugin(MyFindUpdatePlugin)

def main():
    create_option('option.yml')

if __name__ == '__main__':
    main()