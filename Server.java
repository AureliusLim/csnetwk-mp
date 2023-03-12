import java.net.*;
import java.io.*;
import java.util.*;

public class Server {
	public ServerSocket serverSocket;

	public Server(int nPort){
		try{
			this.serverSocket = new ServerSocket(nPort);
		}
		catch(Exception e){
			//e.printStackTrace();
		}
		
	}
	public void startServer(){
		try{
			while(!serverSocket.isClosed()){
				Socket socket = this.serverSocket.accept();
				System.out.println("New Client Connected");// for testing
				ClientHandler clientHandler = new ClientHandler(socket);

				Thread thread = new Thread(clientHandler); // multiple threads for each client
				thread.start();
				
			}
		}
		catch(IOException e){

		}
	}
	public void closeServerSocket(){
		try{
			if(serverSocket != null){
				System.out.println("Server: Connection Terminated");
				serverSocket.close();
			}
		}
		catch(IOException e){
			//e.printStackTrace();
		}
	}
    public static void main(String[] args)
	{
		//int nPort = Integer.parseInt(args[0]);
		System.out.println("Server: Listening on port " + 4000 + "...");

		Server server = new Server(4000);
		server.startServer();
		
	}
}

class ClientHandler implements Runnable{
	public static ArrayList<ClientHandler> clientHandlers = new ArrayList<>();
    private Socket socket;
    private BufferedReader bufferedReader;
    private BufferedWriter bufferedWriter;
    private String clientname;

    public ClientHandler(Socket socket){
        try{
            this.socket = socket;
            this.bufferedWriter = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            this.bufferedReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            this.clientname = "Client";
            clientHandlers.add(this);
           
        }
        catch(IOException e){
            e.printStackTrace();
        }
    }

    @Override
    public void run(){
        String messageFromClient;

        while(socket.isConnected()){
            try{
                String[] command;;
                messageFromClient = bufferedReader.readLine();
                command = messageFromClient.split(" ", 2);
                if(command[0].equals("/leave")){
                    disconnectClient();
                }
                else if(command[0].equals("/register")){
                    this.clientname = command[1];
                }
                
            }
            catch(IOException e){
               //System.out.print(e);
                break;
            }
        }
    }

    public void disconnectClient(){
        System.out.println(this.clientname + " has disconnected");
        clientHandlers.remove(this);
  
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
        }
        catch(IOException e){
            //e.printStackTrace();
        }
    }
}


