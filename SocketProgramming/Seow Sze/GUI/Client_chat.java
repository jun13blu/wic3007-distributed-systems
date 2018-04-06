
import java.io.*;
import java.net.*;
import java.awt.*;
import java.util.*;
import java.awt.event.*;
import javax.swing.*;

public class Client_chat extends JFrame implements ActionListener {
  // Text field for receiving message
  private JTextField jtf = new JTextField();

  // Text area to display contents
  private JTextArea jta = new JTextArea();

  // IO streams
  private DataOutputStream outputToServer;
  private DataInputStream inputFromServer;

  public static void main(String[] args) {
    new Client_chat();
  }

  public Client_chat() {
    // Panel p to hold the label and text field
    JPanel p = new JPanel();
    p.setLayout(new BorderLayout());
    p.add(new JLabel("Enter message"), BorderLayout.WEST);
    p.add(jtf, BorderLayout.CENTER);
    jtf.setHorizontalAlignment(JTextField.LEFT);

    getContentPane().setLayout(new BorderLayout());
    getContentPane().add(p, BorderLayout.SOUTH);
    getContentPane().add(new JScrollPane(jta), BorderLayout.CENTER);

    jtf.addActionListener(this); // Register listener

    setTitle("Client");
    setSize(500, 300);
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    setVisible(true); // It is necessary to show the frame here!

    try {
      // Create a socket to connect to the server
      Socket socket = new Socket("localhost", 10100);

      // Create data input and output streams
      inputFromServer = new DataInputStream(socket.getInputStream());
      outputToServer = new DataOutputStream(socket.getOutputStream());

      while (true) {
        // Receive message from the client
        String message = inputFromServer.readUTF();
        jta.append("Message received from Server: " + message + '\n');
      }      
    }
    catch (IOException ex) {
      jta.append(ex.toString() + '\n');
    }
  }

  public void actionPerformed(ActionEvent e) {
    String actionCommand = e.getActionCommand();
    if (e.getSource() instanceof JTextField) {
      try {
        // Get the radius from the text field
        String message = jtf.getText().trim();

        // Send the radius to the server
        outputToServer.writeUTF(message);
        outputToServer.flush();

        // Display to the text area
        jta.append("Message sent from Client: " + message + "\n"); 
        jtf.setText(null);     
      }
      catch (IOException ex) {
        System.err.println(ex);
      }
    }
  }
}


