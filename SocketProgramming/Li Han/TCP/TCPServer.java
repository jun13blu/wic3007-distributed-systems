import java.net.*;
import java.io.*;
import java.util.Scanner;

public class TCPServer {

   public static void main(String args[]) {

        // Listening port - 10100
        Thread listen = new Thread(new Runnable() {
            @Override
            public void run() {
                Socket clientSocket = null;
                try {
                    int serverPort = 10101;
                    ServerSocket listenSocket = new ServerSocket(serverPort);
                 while(true){
                     DataInputStream input;
                    DataOutputStream output;
                    
                    clientSocket = listenSocket.accept();
                    input = new DataInputStream(clientSocket.getInputStream());
                    output = new DataOutputStream(clientSocket.getOutputStream());
                    String data = input.readUTF();
                    System.out.println("receive from : "
                            + clientSocket.getInetAddress() + ":"
                            + clientSocket.getPort() + " message - " + data);
                   
                 }
                } catch (EOFException e) {
                    System.out.println("EOF: " + e.getMessage());
                } catch (IOException e) {
                    System.out.println("IO: " + e.getMessage());
                } //close socket
                finally {
                    try {
                        clientSocket.close();
                    } catch (IOException e) {/*close failed*/
                    }
                }
            }

        }
        );
        
        Thread send = new Thread(new Runnable() {
            @Override
            public void run() {
                Socket s = null;
                try {
                    int serverPort = 10100;
                    String ip = "localhost";
                    Scanner in = new Scanner(System.in);
                    
                    while(true){
                    String x = in.nextLine();
                    s = new Socket(ip, serverPort);
                    DataInputStream input = new DataInputStream(s.getInputStream());
                    DataOutputStream output = new DataOutputStream(s.getOutputStream());
                    output.writeUTF(x); // UTF is a string encoding

                    System.out.println("Received: " + x);
                    }
                } catch (UnknownHostException e) {
                    System.out.println("Sock:" + e.getMessage());
                } catch (EOFException e) {
                    System.out.println("EOF:" + e.getMessage());
                } catch (IOException e) {
                    System.out.println("IO:" + e.getMessage());
                } finally {
                    if (s != null) {
                        try {
                            s.close();
                        } catch (IOException e) {/*close failed*/
                        }
                    }
                }
            }

        });

        listen.start();

        send.start();

    }
}
