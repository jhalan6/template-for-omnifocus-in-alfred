# -*- coding: utf-8 -*-
import sys
# from pprint import pprint
import os
import json
import commands
import alfred


def byteify(input):
    if isinstance(input, dict):
        return {
            byteify(key): byteify(value) for key, value in input.iteritems()
        }
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, str):
        return input.encode('utf-8')
    else:
        return input


def get_config_from_param(config_name):
    server_config_file = os.path.expanduser('~') + '/.quick_of/config.json'
    with open(server_config_file, 'r') as load_f:
        load_dict = json.load(load_f)
    all_configs = byteify(load_dict)
    return all_configs.get(config_name, {})


def get_user_def_param(params, param_names):
    result = {}
    if len(param_names.split(' ')) != len(params):
        return {}

    for param, param_name in zip(params, param_names.split(' ')):
        result[param_name] = param.decode('utf-8')
    return result


def parse_task_resource_from_config_and_user_def_param(config, user_param):
    result = dict()
    for(k, v)in config.items():
        # parse is the begin of this program, no need to be replaced
        if k == "parse":
            continue

        if type(v) == unicode and "$".decode('utf-8') in v:
            for(param, param_value)in user_param.items():
                v = v.replace("$%s" % param, param_value)

        if type(v) == unicode and v.startswith("!"):
            (status, v) = commands.getstatusoutput("cd ~/.quick_of && %s" %
                                                   v[1:])
        result[k] = v
    return result


def parse_task_resource_to_applescript(task):
    task_properties = """{name:"%s", flagged:%s, sequential: %s}""" % \
        (task.get("name", ""), str(task.get("flagged", False)),
                                   str(task.get("sequential", False)))

    if task.get("inbox", False):
        create_task = """
        set targetTask to make new inbox task with properties %s
        """ % (task_properties)
    elif task.get("folder", ""):
        create_task = """
            set folderMatch to the first item of (folders where name is "%s")
            tell folderMatch
                set targetTask to make project with properties %s
            end tell
        """ % (task.get("folder", ""), task_properties)
    else:
        create_task = """
            set targetTask to make project with properties %s """ \
            % (task_properties)

    add_child_task_script = ""
    if task.get("child task", ""):
        for line in task.get("child task").decode('utf-8').split('\n'):
            add_child_task_script += """
        make task with properties {name:"%s"} """ % (line.replace('"', '\\"'))

    # print create_task
    child_task_script = """
        tell targetTask %s
        end tell""" % (add_child_task_script)

    # print child_task_script
    logic_script = "%s %s" % (create_task, child_task_script)
    result = \
        """tell application "OmniFocus"
        tell default document %s
        end tell
        end tell """ % logic_script
    return result


def main():
    result = []
    config_tag = sys.argv[1]
    query = sys.argv[2:]
    config = get_config_from_param(config_tag)
    if not config:
        result.append(alfred.Item({"uid": alfred.uid(1)},
                                    config_tag, config.get("parse", ""), None))
        alfred.write(alfred.xml(result))
    user_def_param = get_user_def_param(query, config.get("parse", ""))
    if not user_def_param:
        result.append(alfred.Item({"uid": alfred.uid(1)},
                                    config_tag, config.get("parse", ""), None))
        alfred.write(alfred.xml(result))

    task_resource = \
        parse_task_resource_from_config_and_user_def_param(config,
                                                           user_def_param)

    # pprint(config)
    # pprint(user_def_param)
    # pprint(task_resource)
    script = parse_task_resource_to_applescript(task_resource)
    result.append(alfred.Item({"uid": alfred.uid(1), "arg": script},
                                    config_tag, config.get("parse", ""), None))
    alfred.write(alfred.xml(result))

if __name__ == "__main__":
    main()
