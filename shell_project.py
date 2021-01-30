#myshell project - Abe Grogan, ID - 17314893
import cmd,os,sys #modules are imported for use
import platform #mainly used to distinguish OS
import subprocess

class MyShell(cmd.Cmd): #class used for shell
    use_rawinput = False #used to help with using batchfile
    def default(self, args): #runs as a subprocess if the command is not built in
        arg = args.split()
        try:
            if arg[-1] == '&': #runs program as background process
                for i in range(0, len(arg[:-1])):
                    if arg[i] == '>':
                        try:
                            overwrite_file(subprocess.Popen(arg[:i]),arg[i+1:])
                        except IndexError: #if no filename given
                            print('Error: No filename given')
                    elif arg[i] == '>>':
                        try:
                            append_file(subprocess.Popen(arg[:i],arg[i+1])) #use append and overwrite
                        except IndexError:
                            print('Error: No filename given')
                    else:
                        try:
                            subprocess.Popen(arg[:-1])
                        except FileNotFoundError: #if the command doesn't exist
                            print('Error: No such command')

            else:
                try:
                    subprocess.run(arg)
                except FileNotFoundError: #if command doesn't exist
                    print('Error: No such command')
        except IndexError: #given command but no args
            try:
                subprocess.run(arg)
            except FileNotFoundError: #if command doesn't exist
                print('Error: No such command')


    def do_cd(self, args):
        """Changes to your desired directory with ease! You can also use this to find the current directory."""
        if platform.system() == "Windows": #checks os
            os.chdir(args) #sets directory
            prompt.prompt = os.getcwd() + '> ' 
            os.environ['PWD'] = os.getcwd() 
            os.environ['SHELL'] = os.getcwd()+'/MyShell' #sets the prompt and the environment variables pwd and shell
        elif platform.system() == "Linux":

            if len(args) == 0: #if no arg is given, defaults to regular directory
                os.environ['SHELL'] = os.getcwd()+'/MyShell' #sets $SHELL to "(Directory at launch)/MyShell"
                os.environ['PWD'] = os.getcwd()
                if os.environ['HOME'] == os.getcwd()[0:len(os.environ['HOME'])]:
                    prompt.prompt = '{}@{} ~{} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd()[len(os.environ['HOME']):]) #if CWD is in $HOME(/home/user/) display $HOME as "~/" for simplicity.
                else:
                    prompt.prompt = '{}@{} {} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd()) #else show true directory
            else:
                path = args.split() #else its makes the path the new directory and prints new directory
                try:

                    os.chdir(path[0]) #uses split for path and picks first arg, though no need to worry as its split only by spaces
                    os.environ['SHELL'] = os.getcwd()+'/MyShell' #sets $SHELL to "(Directory at launch)/MyShell"
                    if os.environ['HOME'] == os.getcwd()[0:len(os.environ['HOME'])]:
                        prompt.prompt = '{}@{} ~{} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd()[len(os.environ['HOME']):]) #if CWD is in $HOME(/home/user/) show $HOME as "~/" for simplicity. 
                    else:
                        prompt.prompt = '{}@{} {} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd()) #else show true directory

                except FileNotFoundError:
                    print("Error: No such directory") #error message if no directory is found within machine
                except IndexError:
                    os.chdir(os.environ['HOME'])  #if no directory is given, change directory to $HOME
                    if os.environ['HOME'] == os.getcwd()[0:len(os.environ['HOME'])]:    
                        prompt.prompt = '{}@{} ~{} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd()[len(os.environ['HOME']):])  #if CWD is in $HOME(/home/user/) show $HOME as "~/"
                    else:
                        prompt.prompt = '{}@{} {} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd())  #otherwise show true directory

    def do_dir(self, args):
        """lists contents of a directory, or displays current directory content if no arguments are given."""
        args = args.split()  #gets list of command line arguments
        try:
            if args[0] == '<':  #if using standard input
                try:
                    data = from_an_input(args[1])  #use contents of input file as directory
                    try:
                        if args[2] == '>>':  #If using output to append data
                            try:
                                append_file(list_directory(data[0]),args[3:])  #append contents to the file
                            except IndexError:
                                print('Error: No filename given')
                                print('Usage: dir < {} >> <filename>'.format(data[0]))  #shows this error message if no filename specified
                        elif args[2] == '>':
                            try:
                                overwrite_file(list_directory(data[0]), args[3:])  #overwrite the data in the file with the contents
                            except IndexError:
                                print('Error: No filename given')
                                print('Usage: dir < {} >> <filename>'.format(data[0]))  #shows this error message if no filename specified
                        else:
                            print(list_directory(data[0]))  #prints the contents if standard output not being used
                    except IndexError:
                        print(list_directory(data[0]))  #prints the contents if standard output not being used
                except IndexError:
                    print('Error: No filename given')
                    print('Usage: dir < <filename>')  #shows this error message if no filename was specified
            elif args[1] == '>>':  #if using append output with a specific directory
                try:
                    append_file(list_directory(args[0]),args[2:])  #appends the content from the named directory to said filename 
                except IndexError:
                    print('Error: No filename given')
                    print('Usage: dir {} >> <filename>'.format(args[0])) #shows this error if no filename is specified 
            elif args[1] == '>':  #if using overwrite output with a specific directory
                try:
                    overwrite_file(list_directory(args[0]),args[2:])  #overwrites the file's content with the contents of the listed directory
                except IndexError:
                    print('Error: No filename given')
                    print('Usage: dir {} > <filename>'.format(args[0]))  #shows this error if no filename is specified
            elif args[0] == '>>':  #if using append output without a specified directory
                try:
                    append_file([list_directory()],args[1:])  #append the content of the current directory to the specified file
                except IndexError:
                    print('Error: No filename given')
                    print('Usage: dir >> <filename>')  #shows this error message if no filename is specified
            elif args[0] == '>':  #if using overwrite output without a specified directory
                try:
                    overwrite_file([list_directory()],args[1:])  #overwrites file's contents with the content of the current directory
                except IndexError:
                    print('Error: No filename given')
                    print('Usage: dir > <filename>')  #shows this error message if no filename is specified
            else:
                print(list_directory(args[0]))  #prints the content of the specified directory
        except IndexError:
            print(list_directory())  #prints the content of the current directory if no directory is specified

    def do_pause(self, args):
        """pauses shell until user is prompted to resume using enter key"""
        input("press any key to resume.")


    def do_environ(self, args):
        """prints out all enviornment strings."""
        args = args.split()
        try:
            #If you're using overwrite
            if args[0] == '>':
                try:
                    #output environment strings to the specified file
                    overwrite_file(get_environ(), args[1:])
                except IndexError:
                    #print this if no filename is given
                    print('Error: No filename given')
                    print('Usage: environ > <filename>')
            elif args[0] == '>>':
                try:
                    append_file(get_environ(), args[1:]) #appends output to the given file
                except IndexError: #print this Error message if no filename is given
                    print('Error: No filename given')
                    print('Usage: environ >> <filename>')
        except IndexError:
            for environ_var in os.environ:
                print(environ_var + " = " + os.environ[environ_var])

    def do_echo(self, args):
        """displays any comment you input. NOTE: you must have a comment to put in or it will not work"""
        arg = args.split()
        comments = []
        count = 0
        for i in range(0, len(arg)):
            if arg[i] == '>': #if using overwrite
                echoes = get_echo(comments) #concatenate arguments to a string
                try:
                    overwrite_file([echoes], arg[i+1:]) #output the string to the given file
                    break
                except IndexError: #prints this if no filename is given
                    print('Error: No filename given')
                    print('Usage: echo <comment> > <filename>')
                    break
            elif arg[i] == '>>': #if using append
                echoes = get_echo(comments) #concatenate arguments to a string
                try:
                    append_file([echoes], arg[i+1:]) #outputs the string to the said file
                    break
                except IndexError: #prints this if no filename is given
                    print('Error: No filename given')
                    print('Usage: echo <comment> >> <filename>')
                    break
            else:
                comments.append(arg[i]) #appends arguments that are not output commands to a list
                count += 1
        if count == len(arg): #if the loop didn't break early
            print(get_echo(comments)) #print the concatenated list of arguments as a string

    def do_clr(self, args):
        """This clears you're terminal screen. Poof! bye bye long error messages."""
        print("\n" * os.get_terminal_size().lines, end='') #Clears terminal wihtout use of os.system

    def do_help(self,args):
        d = {'dir': (51,55), 'clr':(54,58), 'echo': (57,61), 'cd': (60,64), 'environ': (63,67), 'pause': (66,70), 'help': (69,73), 'quit': (72,76)} #use dictionary to help keep track of command description in manual. 
    
        #NOTE: it's probably a bad idea in practice to hard code line numbers in, since you're manual could expand adding more commands, but since i am at the end of writing my manual, this works better for me, rather than to over engineer a way to pick up where the command paragraphs are.
        
        if 'shell project' in os.getcwd():
            with open("readme",'r') as f:
                contents = f.readlines()
                if len(args) == 0:
                    print("Documented commands (type help <topic>)")
                    print("========================================")
                    string = ""
                    for item in d:
                        string = string + item + "  "
                    
                    print(string)
                elif args == 'more': #if use wants to read whole manual 
                    manual = len(contents) #check size of manual
                    i = 0
                    count = 0 #keeps track to only print 20 lines at a time
                    while i < manual:
                        if count == 20: 
                            count = 0 #reset counter
                            input("press enter to continue") #use input for when user wants to read more
                        print(contents[i].strip())

                        count +=1
                        i+=1

                else:
                    if args in d: #if the argument is a documented command
                        i = d[args][0] #beginning of entry
                        j = d[args][1] #end of entry
                        while i < j:
                            print(contents[i].strip()) #print every line of entry until we reach the end
                            i+=1
                    else: #if command is not documented or doesn't exist
                        print("No help topics for {}".format(args))

        else:
            if platform.system() == 'Windows':
                with open(os.path.expanduser("~\shell project\readme"),'r') as f: 
                    contents = f.readlines()

            else:
                with open(os.path.expanduser("~/shell project/readme"),'r') as f: 
                    contents = f.readlines()
            
            if len(args) == 0:
                print("Documented commands (type help <topic>)")
                print("========================================")
                string = ""
                for item in d:
                    string = string + item + "  "
                    
                print(string)
            elif args == 'more': #if use wants to read whole manual 
                manual = len(contents) #check size of manual
                i = 0
                count = 0 #keeps track to only print 20 lines at a time
                while i < manual:
                    if count == 20: 
                        count = 0 #reset counter
                        input("press enter to continue") #use input for when user wants to read more
                    print(contents[i].strip())

                    count +=1
                    i+=1

            else:
                if args in d: #if the argument is a documented command
                    i = d[args][0] #beginning of entry
                    j = d[args][1] #end of entry
                    while i < j:
                        print(contents[i].strip()) #print every line of entry until we reach the end
                        i+=1
                else: #if command is not documented or doesn't exist
                    print("No help topics for {}".format(args))





    def do_quit(self, args):
        """Quits the program, self explanatory."""
        print ("Now quitting. Thank you for using myShell.") #goodbye message printed before exiting
        raise SystemExit

def get_environ():
    
    env_list = []
    for k in os.environ:
        env_list.append('{} = {}\n'.format(k, os.environ[k])) #appends environ variables to a list an retuns it
    return env_list


def get_echo(comment):
    return " ".join(comment) #concatenates to a single string


def list_directory(directory=None):
    try:
        if  directory != None:  #if a directory is specified
            return  "\n".join([f for f in os.listdir(directory)]) #return a string containing all the contents of the specified directory
        else:   #If no directory is specified
            return '\n'.join([f for f in os.listdir()])  #return a string containing the contents of the current directory

    except FileNotFoundError:
        #print this if no such directory exists
        print('Error: Directory "{}" not found'.format(directory))  #shows this error message if the directory does not exist
        


def from_an_input(file):
    try:
        with open(file,'r') as f:
            return [args.strip() for args in f.readlines()] #returns a list of all the lines contained in the file
    except FileNotFoundError:
        print('Error: File "{}" not found'.format(file))  #shows this error message if the file does not exist


def overwrite_file(data,args):

    try:
        with open(args[0], 'w+') as f:  #opens the file, or creates one with that name if it doesn't exist
            for a in data:
                f.write(a)  #writes the data to the file, overwriting any data that was already contained by the file 
            f.write('\n')  #adds a newline character to the end of the file
    except IndexError:
        print('Usage: <command> > <filename>')  #shows this error message if no file was specified


def append_file(data,args):
    try:
        with open(args[0], 'a+') as f:  #opens the file, or creates one with that name if it doesn't exist
            for a in data:
                f.write(a)  #writes the data to the file, appending to the end of the file if there was already data within the file
            f.write('\n')  #adds a newline charater to the end of the file
    except IndexError:
        print('Usage: <command> >> <filename>')  #shows this error message if no filename was specified
        



if __name__ == '__main__':
    prompt = MyShell()
    if platform.system() == "Windows": #if os is windows
        if len(sys.argv) > 1: #if a batchfile is given
            with open(sys.argv[1], 'r') as f: #open file
                shell = MyShell() #start an instance of myshell 
                batchfile = f.readlines() #create a list of commands
                batchfile.append('quit')
                shell.cmdqueue = batchfile
                shell.prompt = os.getcwd() + '> ' #set prompt
                shell.cmdloop() #run batchfile
        else:
            prompt.prompt = os.getcwd() + '> ' #easy way to display path in shell
    else:
        os.environ['SHELL'] = os.getcwd()+'/MyShell'  #Sets $SHELL to "(Directory at launch)/MyShell"
        if len(sys.argv) > 1: #if batchfile is given
            with open(sys.argv[1], 'r') as f: #open file
                batchfile = MyShell(stdin=f) #start an instance of myshell with the file as standard input
                if os.environ['HOME'] == os.getcwd()[0:len(os.environ['HOME'])]:
                    batchfile.prompt = '{}@{} ~{} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd()[len(os.environ['HOME']):])  #If CWD is in $HOME(/home/user/) display $HOME as "~/" for simplicity.
                else:
                    batchfile.prompt = '{}@{} {} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd())  #else display true directory
                batchfile.cmdloop() #runs batchfile
        else:
            if os.environ['HOME'] == os.getcwd()[0:len(os.environ['HOME'])]:
                prompt.prompt = '{}@{} ~{} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd()[len(os.environ['HOME']):])  #If CWD is in $HOME(/home/user/) display $HOME as "~/" for simplicity.
            else:
                prompt.prompt = '{}@{} {} $ '.format(os.environ['USER'],os.uname()[1],os.getcwd())  #else display true directory
    prompt.cmdloop("Welcome to myShell! if you're finding trouble with myShell, please use the help command.")

