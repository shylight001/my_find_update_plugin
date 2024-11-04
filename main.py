from my_find_update_plugin.my_find_update_plugin import MyFindUpdatePlugin
from jmcomic import create_option, JmModuleConfig
import sys
import io

# Change the stdout encoding to UTF-8
if sys.stdout.encoding != 'utf-16':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-16')

JmModuleConfig.register_plugin(MyFindUpdatePlugin)

def main():
    create_option('option.yml')

if __name__ == '__main__':
    main()