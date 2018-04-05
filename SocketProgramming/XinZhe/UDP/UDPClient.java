import java.net.*;
import java.io.*;
import java.util.Scanner;

public class UDPClient {    // Modified, ready to chat!

    public static void main(String args[]) {

        // Listening port - 11100
        Thread listen = new Thread(new Runnable() {
            @Override
            public void run() {
                DatagramSocket aSocket = null;
                try {
                    System.out.println("start client...");
                    aSocket = new DatagramSocket(11100);
                    byte[] buffer = new byte[1000];
                    while (true) {
                        DatagramPacket request = new DatagramPacket(buffer, buffer.length);
                        //listening incoming request
                        aSocket.receive(request);
                        System.out.println("receive from : " +
                                request.getAddress().toString() + ":" + request.getPort() +
                                " message - " + new String(request.getData()).trim());
                    }
                } catch (SocketException e) {
                    System.out.println("Socket: " + e.getMessage());
                } catch (IOException e) {
                    System.out.println("IO: " + e.getMessage());
                }
                //close socket
                finally {
                    if (aSocket != null) aSocket.close();
                }
            }
        });
        // Sending port - 10100
        Thread send =  new Thread(new Runnable() {
            @Override
            public void run() {
                DatagramSocket aSocket = null;
                try {
                    int serverPort = 10100;
                    String ip = "localhost";
                    InetAddress aHost = InetAddress.getByName(ip);
                    try {
                        while (true) {
                            aSocket = new DatagramSocket();
                            Scanner scanner = new Scanner(System.in);
                            String message = scanner.nextLine();
                            DatagramPacket request =
                                    new DatagramPacket(message.getBytes(), message.length(), aHost, serverPort);
                            //send a message to server
                            aSocket.send(request);
                            System.out.println("send to : " + request.getAddress() + ":" +
                                    request.getPort() + " message - " + new String(request.getData()).trim());
                        }
                    } catch (SocketException e) {
                        System.out.println("Socket: " + e.getMessage());
                    }

                } catch (IOException e) {
                    System.out.println("IO: " + e.getMessage());
                }
            }
        });

        listen.start();
        send.start();

    }
}

        

