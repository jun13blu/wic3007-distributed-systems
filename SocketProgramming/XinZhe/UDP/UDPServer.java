// UDPServer.java
// A server program implementing UDP socket

import java.net.*;
import java.io.*;
import java.util.Scanner;

public class UDPServer {    // Modified, ready to chat!

    public static void main(String args[]) {

        // Listening port - 10100
        Thread listen = new Thread(new Runnable() {
            @Override
            public void run() {
                DatagramSocket aSocket = null;
                try {
                    System.out.println("start server...");
                    //create a datagram socket using port 10100
                    aSocket = new DatagramSocket(10100);
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
        // Sending port - 11100
        Thread send = new Thread(new Runnable() {
            @Override
            public void run() {
                DatagramSocket aSocket = null;
                try {
                    int clientPort = 11100;
                    String ip = "localhost";
                    InetAddress aHost = InetAddress.getByName(ip);
                    try {
                        while (true) {
                            aSocket = new DatagramSocket();
                            Scanner scanner = new Scanner(System.in);
                            String message = scanner.nextLine();
                            DatagramPacket request =
                                    new DatagramPacket(message.getBytes(), message.length(), aHost, clientPort);
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

