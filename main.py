"""The main logic of the application.

Only native files are used, without direct import of libraries.
The whole program is on top, without diving into the details.

imports:


"""
from datetime import datetime
# from bin.GUI import create_main_window


# It is using in name files: logs and output .docx
TIME_START_PROG = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')


def write_to_log(error_massage, fn_name=None, filename=None, line_number=None):
    """My simple program logging implementation

    :param error_massage: Contents and explanation of the error
    :type error_massage: str
    :param fn_name: The name of the function inside which the error occurred
    :type fn_name: str
    :param filename: The name of the file where the error occurred
    :type filename: str
    :param line_number: The line number where the log entry was called
    :type line_number: int
    :return: Adding information about a new error to the logs file
    :rtype: None

    """
    time_of_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('program_logs.txt', "a+") as log:
        template = f"[{time_of_log}] fn {fn_name} from {filename} " \
                   f"line is {line_number}\n" \
                   f"Error: {error_massage}\n\n"

        log.write(template)


# ToDo: It is not necessary function - remove it before publication
def time_report_and_logger(fn):
    """The name of the function and the time of its operation is output to the console
    and recorded in the log (creates a new file by starting datetime).
    It's decorator for any fns.

    :return fn: The name of any function
    :rtype fn: object
    :return: Function wrapped of time loging
    :rtype: object

    """
    def wrapper(*args, **kwargs):
        """Wrapper of function, write time in lig file and display parameters
        into terminal.

        :param args: Arguments for our function
        :type args: any
        :param kwargs: Kwargs for our function
        :type kwargs: any
        :return: Result of our function
        :rtype: Depends on our function

        """
        fn_name = str(fn).split()[1]
        time_start = datetime.now()

        print(f'START: {fn_name}')


        result = fn(*args, **kwargs)


        time = datetime.now() - time_start

        print(f'FINISH\n'
              f'PROCESS TIME: {time}\n')

        with open(f'time_logs__{TIME_START_PROG}__.txt', 'a+') as log:
            log.write(f'FN:{fn_name},TIME:{time}\n')

        return result

    return wrapper


if __name__ == '__main__':
    pass
    # # Creating the entire gui
    #
    # window = create_main_window()
    #
    # window.mainloop()
