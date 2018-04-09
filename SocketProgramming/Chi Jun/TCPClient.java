import java.net.*;
import java.io.*;
import java.util.Scanner;

import javax.sound.midi.Soundbank;

public class TCPClient {
	public static void main(String args[]) {
		Socket s = null;
		try {
			int serverPort = 10100;
			String ip = "localhost";
			s = new Socket(ip, serverPort);
			Connection listen = new Connection(s, "listen");
			Connection write = new Connection(s, "write");
		} catch (UnknownHostException e) {
			System.out.println("Sock:" + e.getMessage());
		} catch (IOException e) {
			System.out.println("Connection:" + e.getMessage());
		}
	}

	static class Connection extends Thread {
		DataInputStream input;
		DataOutputStream output;
		Socket serverSocket;
		String type;

		public Connection(Socket aServerSocket, String aType) {
			try {
				serverSocket = aServerSocket;
				input = new DataInputStream(serverSocket.getInputStream());
				output = new DataOutputStream(serverSocket.getOutputStream());
				type = aType;
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
						System.out.println(data);
					}
				} else {
					while (true) {
						Scanner in = new Scanner(System.in);
						String text = in.nextLine();
						if (text.length() > 0) {
							output.writeUTF(text);
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
					serverSocket.close();
				} catch (IOException e) {
					/*close failed*/}
			}
		}
	}
}
