import java.io.*;
import java.net.*;
import java.util.*;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;

public class clientChat extends JFrame implements ActionListener {
	static Socket socket;
	JPanel p;
	JTextField jtf;
	JTextArea jta;
	JButton Send;

	public clientChat() throws UnknownHostException, IOException {
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
		Send.addActionListener(this);
		socket = new Socket(InetAddress.getLocalHost(),10100);

		jta.setText("Connected to Server");
		this.setTitle("Client");
		while (true) {
			try {
				DataInputStream dis = new DataInputStream(socket.getInputStream());
				String string = dis.readUTF();
				jta.setText(jta.getText() +"\n Server:"
						+ string);
			} catch (Exception e1) {
				jta.setText(jta.getText() + "\n Message sending fail:Network Error");
			}
		}
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		if ((e.getSource() == Send) && (jtf.getText() != "")) {

			jta.setText(jta.getText() + "\n Me:"
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
		clientChat chatForm = new clientChat();
	}
}