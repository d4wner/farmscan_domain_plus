#coding=utf-8

from importlib import import_module
import argparse

class domain_get:
    def __init__(self, args):
        self.modules = [
            'api_subdomain_search',
            'gitleak',
            'search_engine_spider'
        ]
        self.domain = args.domain
        self.output = args.output

    def exploit(self):
        for module in self.modules:
            handler = import_module(module)
            multi_list = handler.exploit(self.domain)
            with open(self.output, 'a+') as f:
                for line in multi_list:
                    f.writelines(line + '\n')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='[+]Hellfarm v1.1')
    parser.add_argument('-u' , '--domain',  type=str,  help='Url you wish to fuzz')
    #parser.add_argument('-t' , '--thread',  type=int,  default=10,  help='Threads for this bitch script')
    parser.add_argument('-o', '--output',  type=str,    help="Output name for this scan")
    args = parser.parse_args()

    handler = domain_get(args)
    handler.exploit()