import java.io.*;
import java.net.*;
import java.util.*;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class serverChat extends JFrame implements ActionListener {
	static ServerSocket server;
	static Socket socket;
	JPanel p;
	JTextField jtf;
	JTextArea jta;
	JButton Send;
	DataInputStream dis;
	DataOutputStream dos;

	public serverChat() throws UnknownHostException, IOException {

		p = new JPanel();
		jtf = new JTextField();
		jta = new JTextArea();
		Send = new JButton("Send");
		this.setSize(500, 500);
		this.setVisible(true);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		p.setLayout(new BorderLayout());
		p.add(jtf,BorderLayout.CENTER);
		p.add(Send,BorderLayout.EAST);
		jtf.setHorizontalAlignment(JTextField.RIGHT);
		getContentPane().setLayout(new BorderLayout());
		getContentPane().add(p, BorderLayout.NORTH);
		getContentPane().add(new JScrollPane(jta), BorderLayout.CENTER);
		this.setTitle("Server");
		Send.addActionListener(this);
		server = new ServerSocket(10100, 1, InetAddress.getLocalHost());
		jta.setText("Waiting for Client");
		socket = server.accept();
		jta.setText(jta.getText() + "\n Client Found");
		while (true) {
			try {
				DataInputStream dis = new DataInputStream(socket.getInputStream());
				String string = dis.readUTF();
				jta.setText(jta.getText() +"\n Client:"
						+ string);
			} catch (Exception e1) {
				jta.setText(jta.getText() + "\n Message sending fail:Network Error");
				
			}
		}
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		if ((e.getSource() == Send) && (jtf.getText() != "")) {
			jta.setText(jta.getText() +"\n ME:"
					+ jtf.getText());
			try {
				DataOutputStream dos = new DataOutputStream(
						socket.getOutputStream());
				dos.writeUTF(jtf.getText());
			} catch (Exception e1) {
				System.err.println(e1);
			}
			jtf.setText("");
		}
	}

	public static void main(String[] args) throws UnknownHostException,
	IOException {
		new serverChat();
	}
}