import parser_lib.lexer as lexer
import parser_lib.parser as parser 
import type_lib
import helper
import argparse

import settings


#################### Reading Source File ####################
def read_text_file(address):
    with open(address, 'r') as file:
        data = file.read()
    return data


#################### Extract the Dependencies ####################
def extract_dependencies(_source_address):
    data = read_text_file(_source_address)
    lx = lexer.Lexer(data)
    prs = parser.Parser(lx)
    prg_out = prs.parse_program()

    settings.DB_SCHEMA = prg_out["table_defs"]

    policy_defs = prg_out["policy_defs"]
    policy_labels = helper.sts_policy(policy_defs)

    prg_ast = prg_out["stm_list"]

    prg_vars = helper.compute_vars(prg_ast)
    gamma_f = type_lib.Gamma(prg_ast, prg_vars)
    program_labels = helper.sts(gamma_f.env[settings.OBSERVER])

    if settings.DEBUG:
        print("Gamma final : " + str(gamma_f))
        print()
        print(settings.OBSERVER+"'s Dependency:\n\t"+settings.OBSERVER+" ↦ " + helper.str_forzensets(gamma_f.env[settings.OBSERVER]))
        print()
        print("Program Labels : " + str(program_labels))
        print()
        print("Policy Labels : " + str(policy_labels))
        print()

    check_security(policy_labels, program_labels)
            

def check_security(_policy_labels, _program_labels):
    secure = True
    for prg_label in _program_labels:
        if (not is_allowed(prg_label,_policy_labels)):
            secure = False
            # TODO, add more info on why

    if secure:
        print("\n>>> The program is secure.")
    else:
        print("\n>>> The program is insecure.")


def is_allowed(_prg_label, _policy_labels):
    if not _policy_labels:
        print(">>> No Policy!")
        return True
    
    for pol_label in _policy_labels:
        if (_prg_label.is_less_than(pol_label)):
            return True
    return False


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-i", "--input", type=str, help="Address the of source code")
    arg_parser.add_argument("-o", "--observer", type=str, help="The observer's variable'")
    arg_parser.add_argument('-d', action='store_true', help='Enable debug mode')
    args = arg_parser.parse_args()

    if args.d:
        settings.DEBUG = True
    if args.observer:
        settings.OBSERVER = args.observer

    if args.input:
        extract_dependencies(args.input)
    else:
        print(">>> Please provide the address of the source code")
        print()
        arg_parser.print_help()

