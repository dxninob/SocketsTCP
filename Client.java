import java.net.Socket;
import java.util.Scanner;
import java.io.*;

public class Client {

    // Define server IP address and port
    static String server = "127.0.0.1";
    static int port = 80;
    // Create scanner to read data from the console
    static Scanner sc = new Scanner(System.in);;
    // Define variables that most methods in the class will use
    static Socket socket;
    static PrintStream out;
    static BufferedReader in;

    public static void main(String[] args) {
        try {
            System.out.println("Client is running...");
            // Connect to the server
            socket = new Socket(server, port);

            // Create input and output streams to read from and write to the server
            out = new PrintStream(socket.getOutputStream());
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            System.out.println("Enter \"QUIT\" to exit\n");
            System.out.println("Input commands:");
            
            while (true) {
                // Read command from console
                String command_to_send = sc.nextLine();
                if (command_to_send.equals("")) {
                    System.out.println("Please input a valid command...");
                } else {
                    // Send the command to the server
                    out.println(command_to_send);

                    // If command is QUIT, break while cycle and close connection
                    if (command_to_send.equals("QUIT")) {
                        break;
                    }

                    // Split the command into words
                    String[] command_words = command_to_send.split("\\s+");
                    // If the command does not have two words, it is an valid command
                    if (command_words.length == 2) {
                        // Select HTTP method to be executed
                        methods(command_words[0], command_words[1]);
                    } else {
                        // Read server response if the input is an invalid method 
                        String firstLine = readHeader();
                    }          
                }
                System.out.println();
            }
            System.out.println("Closing connection...BYE BYE...");
            // Close our streams
            in.close();
            out.close();
            // Close connection to the server
            socket.close();
        } catch(Exception e) {
                e.printStackTrace();
        }
    }

    public static void methods (String method, String myfile) {
        if (method.equals("GET")) {
            try {
                // Read data from the server until we finish reading the document
                String firstLine = readHeader();
                // Read file if it exists
                if (!firstLine.equals("404 Not Found")) {
                    // Create file in client
                    myfile = getFileName(myfile);
                    File fileOutput = new File(myfile);
                    // Create output stream to write in the file
                    FileOutputStream output = new FileOutputStream(fileOutput);
                    // Read file data
                    String line = in.readLine();
                    while(!line.equals("")) {
                        output.write(line.getBytes());
                        output.write('\n');
                        line = in.readLine();
                    }
                    output.close();
                }
            }  catch(Exception e) {
                e.printStackTrace();
            }
        } else if (method.equals("HEAD")) {
            String firstLine = readHeader();
        }  else if (method.equals("POST")) {
            try {
                // Read and print message from the server
                String line = in.readLine();
                System.out.println(line);
                String variable = "";
                // Stop receiving and sending data when the client write "END"
                while(!variable.equals("END")) {
                    line = in.readLine();
                    System.out.println(line);
                    // Read variable/value from the scanner and send it to the server
                    variable = sc.nextLine();
                    out.println(variable);
                }
                // Read HTTP response header
                String firstLine = readHeader();
            } catch(Exception e) {
                e.printStackTrace();
            }
        } else {
            String firstLine = readHeader();
        }
    }

    public static String readHeader() {
        try {
            String line = in.readLine();
            String firstLine = line;
            while(!line.equals("")) {
                System.out.println(line);
                line = in.readLine();
            }
            return firstLine;
        } catch(Exception e) {
            e.printStackTrace();
            return e.toString();
        }
    }

    public static String getFileName(String myfile) {
        if(myfile.equals("/")) {
            return "index.html";
        } else {
            //return the name of the file
            String[] f = myfile.split("/");
            return f[f.length - 1];
        }
    }

}