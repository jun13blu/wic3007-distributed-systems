import java.net.*;
import java.io.*;
import java.util.Scanner;

public class TCPServer {

    public static void main(String args[]) {
        try {
            int serverPort = 10100;
            ServerSocket listenSocket = new ServerSocket(serverPort);

            System.out.println("server start listening...");
            while (true) {
                Socket clientSocket = listenSocket.accept();
                Connection listen = new Connection(clientSocket, "listen");
                Connection write = new Connection(clientSocket, "write");
            }
        } catch (IOException e) {
            System.out.println("Listen :" + e.getMessage());
        }
    }

    static class Connection extends Thread {
        DataInputStream input;
        DataOutputStream output;
        Socket clientSocket;
        String type;

        public Connection(Socket aClientSocket, String aType) {
            try {
                type = aType;
                clientSocket = aClientSocket;
                input = new DataInputStream(clientSocket.getInputStream());
                output = new DataOutputStream(clientSocket.getOutputStream());
                this.start();
            } catch (IOException e) {
                System.out.println("Connection:" + e.getMessage());
            }
        }

        public void run() {
            try { // an echo server 
                if (type.equals("listen")) {
                    while (true) {
                        String data = input.readUTF();
                        System.out.println("\nreceive from : " + clientSocket.getInetAddress() + ":"
                                + clientSocket.getPort() + " message - " + data + "\n");
                    }
                } else {
                    while (true) {
                        Scanner in = new Scanner(System.in);
                        String text = in.nextLine();
                        if (text.length() > 0) {
                            output.writeUTF("\nreceive from : " + clientSocket.getInetAddress() + ":"
                                    + clientSocket.getPort() + " message - " + text + "\n");
                            System.out.println();
                        }
                    }
                }
            } catch (EOFException e) {
                System.out.println("EOF:" + e.getMessage());
            } catch (IOException e) {
                System.out.println("IO:" + e.getMessage());
            }

            finally {
                try {
                    clientSocket.close();
                } catch (IOException e) {
                    /*close failed*/}
            }
        }
    }
}
