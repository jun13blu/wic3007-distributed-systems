
import java.io.*;
import java.net.*;
import java.util.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class Server_chat extends JFrame implements ActionListener {
  // Text area for receiving message
  private JTextField jtf = new JTextField();

  // Text area for displaying contents
  private JTextArea jta = new JTextArea();

  private DataOutputStream outputToClient;
  private DataInputStream inputFromClient;

  public static void main(String[] args) {
    new Server_chat();
  }

  public Server_chat() {
    // Place text area on the frame
    JPanel p = new JPanel();
    p.setLayout(new BorderLayout());
    p.add(new JLabel("Enter message"), BorderLayout.WEST);
    p.add(jtf, BorderLayout.CENTER);
    jtf.setHorizontalAlignment(JTextField.LEFT);

    getContentPane().setLayout(new BorderLayout());
    getContentPane().add(p, BorderLayout.SOUTH);
    getContentPane().add(new JScrollPane(jta), BorderLayout.CENTER);

    jtf.addActionListener(this); // Register listener

    setTitle("Server");
    setSize(500, 300);
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setVisible(true); // It is necessary to show the frame here!

    try {
      // Create a server socket
      ServerSocket serverSocket = new ServerSocket(10100);
      jta.append("Server started at " + new Date() + '\n');

      // Listen for a connection request
      Socket socket = serverSocket.accept();
      //System.out.println("Received connection: "+socket.getRemoteSocketAddress());

      // Create data input and output streams
      inputFromClient = new DataInputStream(socket.getInputStream());
      outputToClient = new DataOutputStream(socket.getOutputStream());

      while (true) {
        // Receive message from the client
        String message = inputFromClient.readUTF();
        jta.append("Message received from client: " + message + '\n');
      }
    }
    catch(IOException ex) {
      System.err.println(ex);
    }
  }

  public void actionPerformed(ActionEvent e) {
    String actionCommand = e.getActionCommand();
    if (e.getSource() instanceof JTextField) {
      try {
        // Get the radius from the text field
        String message = jtf.getText().trim();

        // Send the radius to the server
        outputToClient.writeUTF(message);
        outputToClient.flush();

        jta.append("Message sent from server: " + message + "\n");
        jtf.setText(null);
      }
      catch (IOException ex) {
        System.err.println(ex);
      }
    }
  }
}
