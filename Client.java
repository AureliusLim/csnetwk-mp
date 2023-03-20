
import java.net.*;
import java.io.*;
import java.util.*;
public class Client {
	private Socket socket;
	private BufferedReader bufferedReader;
	private BufferedWriter bufferedWriter;
	private String username;
	public Client(Socket socket, String username){
		try{
			this.socket = socket;
			this.bufferedWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			this.bufferedReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			this.username = username;
			System.out.println("Connection to the Message Board Server is Succcessful!");
		}
		catch(IOException e){
			e.printStackTrace();
		}
	}
	public void sendMessage(){
		try{
			
			Scanner scanner = new Scanner(System.in);
			
			while(socket.isConnected()){
				String messageToSend = scanner.nextLine();
				String[] command;;
             
                command = messageToSend.split(" ", 2);
				bufferedWriter.write(messageToSend);
				bufferedWriter.newLine();
				bufferedWriter.flush();
					
                if(command[0].equals("/leave")){ // leave
					disconnectClient();
                }
                else if(command[0].equals("/register")){ //set alias
                    this.username = command[1];
                }
			  
				

			}
		}
		catch(IOException e){
			//e.printStackTrace();
		}
	}
	public void listenForMessage(){
		new Thread (new Runnable(){
			@Override public void run(){
				String message;
				while(socket.isConnected()){
					try{
						message = bufferedReader.readLine();
						System.out.println(message);
					}
					catch(Exception e){
						e.printStackTrace();
					}
				}
			}
		}).start();
	}
	public void disconnectClient(){
		System.out.println("Connection Closed. Thank you!");
        try{
            if(this.bufferedReader != null){
                this.bufferedReader.close();
            }
            if(this.bufferedWriter!= null){
                this.bufferedWriter.close();
            }
            if(this.socket != null){
                socket.close();
            }
			System.exit(0);
        }
        catch(IOException e){
            //e.printStackTrace();
        }
	}
    public static void main(String[] args)
	{
		try{
			Scanner scanner = new Scanner(System.in); // parse "/join localhost 4000"
			String connection = scanner.nextLine();
			String[] formatted = connection.split(" ");
			int nport = Integer.parseInt(formatted[2]);
			Socket socket = new Socket(formatted[1], nport);

			Client client = new Client(socket, "Client");
			client.listenForMessage();
			client.sendMessage();
		}
		catch(Exception e){
			//e.printStackTrace();
			System.out.println("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.");
		}
		
	}
}
