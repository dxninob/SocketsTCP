import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;
import java.util.Scanner;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.io.File;

public class Client {

    static Scanner sc;
    static Socket socket;
    static PrintStream out;
    static BufferedReader in;

    public static void main(String[] args) {
        String server = "127.0.0.1";
        int port = 80;
        sc = new Scanner(System.in);

        System.out.println("Client is running...");
        try {
            // Connect to the server
            socket = new Socket(server, port);
            // System.out.println("Connected to the server from:");

            // Create input and output streams to read from and write to the server
            out = new PrintStream(socket.getOutputStream());
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            System.out.println("Enter \"QUIT\" to exit\n");
            System.out.println("Input commands:");
            String command_to_send = sc.nextLine();

            while (true) {
                if (command_to_send.equals("")) {
                    System.out.println("Please input a valid command...");
                } else {
                    out.println(command_to_send);

                    if (command_to_send.equals("QUIT")) {
                        break;
                    }

                    String[] command_words = command_to_send.split("\\s+");
                    if (command_words.length == 2) {
                        methods(command_words[0], command_words[1]);
                    } else {
                        String line = in.readLine();
                        while(!line.equals("")) {
                            System.out.println(line);
                            line = in.readLine();
                        }
                    }          
                }
                System.out.println();
                command_to_send = sc.nextLine();
            }
            System.out.println("Closing connection...BYE BYE...");
            // Close our streams
            in.close();
            out.close();
            socket.close();
        } catch(Exception e) {
                e.printStackTrace();
        }
    }

    public static void methods (String method, String myfile) {
        if (method.equals("GET")) {
            try {
                // Read data from the server until we finish reading the document
                String line = in.readLine();
                String firstLine = line;
                while(!line.equals("")) {
                    System.out.println(line);
                    line = in.readLine();
                }
                if (!firstLine.equals("HTTP/1.1 404 Not Found")) {
                    File fileOutput = new File("archivo2.txt");
                    FileOutputStream output = new FileOutputStream(fileOutput);
                    line = in.readLine();
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
            
        }  else if (method.equals("POST")) {
    
        } else if (method.equals("PUT")) {
            
        } else {
            try {
            String line = in.readLine();
                while(!line.equals("")) {
                    System.out.println(line);
                    line = in.readLine();
                }
            }  catch(Exception e) {
                e.printStackTrace();
            }
        }
    }

}