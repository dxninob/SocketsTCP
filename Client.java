import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;
import java.util.Scanner;

public class Cliente {

    public static void main(String[] args) {
        String server = "127.0.0.1";
        int port = 80;
        Scanner sc = new Scanner(System.in);

        System.out.println("Client is running...");
        try {
            // Connect to the server
            Socket socket = new Socket(server, port);
            // System.out.println("Connected to the server from:");

            // Create input and output streams to read from and write to the server
            PrintStream out = new PrintStream(socket.getOutputStream());
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            System.out.println("Enter \"QUIT\" to exit\n");
            System.out.println("Input commands:");
            String command_to_send = sc.nextLine();

            while (true) {
                if (command_to_send.equals("")) {
                    System.out.println("Please input a valid command...");
                } else {
                    out.println(command_to_send);

                    // Read data from the server until we finish reading the document
                    // FALTA: NO LEE MUCHAS LINEAS
                    String line = in.readLine();
                    while(!line.equals("")) {
                        System.out.println(line);
                        line = in.readLine();
                    }

                    if (command_to_send.equals("QUIT")) {
                        break;
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

}