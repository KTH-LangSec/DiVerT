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
        print("#"*25+" DEBUG "+"#"*25)
        print("Gamma final : " + str(gamma_f))
        print()
        print(settings.OBSERVER+"'s Dependency:\n\t\t"+settings.OBSERVER+" ↦ " + helper.str_forzensets(gamma_f.env[settings.OBSERVER]))
        print()
        print("Program Labels : " + helper.str_label_set(program_labels))
        print()
        print("Policy Labels : " + helper.str_label_set(policy_labels))
        print()

    check_security(policy_labels, program_labels)
            

def check_security(_policy_labels, _program_labels):
    secure = True
    for prg_label in _program_labels:
        result, reason = is_allowed(prg_label,_policy_labels)
        if (not result):
            secure = False
            if (settings.REASON):
                print("#"*25+" REASON(S) "+"#"*25)
                print("Because: "+ reason)
            break

    print("#"*25+" VERDICT "+"#"*25)
    if secure:
        print("\n>>> The program is secure. ✓\n")
    else:
        print("\n>>> The program is insecure. ⨉\n")


def is_allowed(_prg_label, _policy_labels):
    if not _policy_labels:
        return False, "No policy definition was found!"
    
    res = ""
    for pol_label in _policy_labels:
        result, reason = _prg_label.is_less_than(pol_label)
        if (result):
            return True, "Secure"
        else:
            res += str(reason)

    return False, res


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-i", type=str, help="Address the of source code")
    arg_parser.add_argument("-o", type=str, help="The observer's identifier (e.g. u)")
    arg_parser.add_argument('-d', action='store_true', help='Enable debug mode (prints gamma, program and policy labels)')
    arg_parser.add_argument('-r', action='store_true', help='Prints the reasons for rejecting the program')
    args = arg_parser.parse_args()

    if args.d:
        settings.DEBUG = True
    if args.r:
        settings.REASON = True
    if args.o:
        settings.OBSERVER = args.observer

    if args.i:
        extract_dependencies(args.i)
    else:
        print(">>> Please provide the address of the source code")
        print()
        arg_parser.print_help()

