

import java.io.PrintStream;

import java.util.Random;

import java.util.Scanner;



public class Speedrun {
	public static void main(final String args[]) {
		
        System.out.println("Hey, welcome to speedrun! This game is played with 2 players.");
        // We made a player class, we tried to do more than two players but we didn't succeed, so we did it with two players.
      
        
        final Scanner scanner = new Scanner(System.in);
        //this gives the input for the player
        final Random random = new Random();
        
        // We play the game with 2 players, 
        //we gave some values to the player class
        final Player player1 = new Player(1, random, scanner, System.out);
        final Player player2 = new Player(2, random, scanner, System.out);
        
        
       
        //we print the winner of the game with the wile and if statement, we print the winner of the game,
        
        //if takeTurn (from the player class, see this class to clarify) is true for player 1,
        //than we print that player 1 is the winner and we break the loop. If takeTurn is true  for player 2,
        // we print that player 2 is the winner and we break the loop
        
        while (true) {
            if (player1.takeTurn()) {
                System.out.println(player1.getName() + " wins!");
                break;
            }
            if (player2.takeTurn()) {
                System.out.println(player2.getName() + " wins!");
                break;
            }
        }

    }

	private static class Player {
		
		

		//we defined variables in the new class, we use the final keyword as well, 
		//we are using this because we want the variables always store the same values after the values are assignd to them
		
	    final Random random;
	    
	    final String name;
	    
	    final Scanner scanner;
	    
	    final PrintStream output;
	    int score;
	    
	    
	    Player(final int id, final Random random, final Scanner scanner, final PrintStream output) {
	        this.name = "Player " + id;
	        this.random = random;
	        this.scanner = scanner;
	        this.output = output;
	      //above you can see how the values are assigned.You can see we have used the 'this' keyword. This is to refer to the current object. 
	        //This is to avoid naming conflicts in the constructors of the objects.
	    }
	    
	   
	    
	    public boolean takeTurn() {
	    	//above boolean takeTurn is defined
	    	//in the DiceTo100 class takeTurn is used to determine the winner of the game
	    	// First we tell which player's turn it is
	    	
	        this.output.println(this.name + "'s turn to roll");
	        
	      
	        // we ask the player if he wnts to roll the dice, he can choose between y and n
	        this.output.println("Do you want to play this turn? (Y/N)");
	        //If the answers equals N, which means no, we print that this player skipped his turn and we return false, because this is a boolean expression
	        if (this.answer().equals("N")) {
	            this.output.println(this.name + " skipped their turn.");
	            return false;
	        }
	        
	        
	        // here we set the current score in the turn. 
	        int currentRoundScore = 0;
	        // next we have a do while statement. 
	        do {
	        	
	        	
	            final int roll = this.random.nextInt(6) + 1;
	            // we create the roll variable. This is to recreate a dice, getting a number between 1 and 6 (therefore we do +1)
	            //then we print the outcome of the roll (getting a random integer between 1 and 6)
	            this.output.println(this.name + " rolled a " + roll);
	            //what we roll, we add to the current score of this round
	            currentRoundScore += roll;
	            //next we will have an if statement. If the roll equals 1, 
	            //the current score of the round will be set to 0 and then break the loop.
	            if (roll == 1) {
	                currentRoundScore = 0;
	                break;
	                
	                
	            }
	            //after the break, we will print the score of the round. 
	            //This will be zero after roll == 1 or a specific amount after a number of rolls after a turn has ended before rolling a 1
	            this.output.println(this.name + "'s score this turn is " + currentRoundScore);
	            //the do while statement will keep going if the current score + the current round score is less than 100 and if boolean continueRolling is true. 
	            //This is defined later in the code
	        } while (((this.score + currentRoundScore) < 100) && this.continueRolling());
	        
	        // the current round score will be added to the score and the total score will be printed. 
	        //So, this can be after a player has reached 100 points or when a players decides to end his or her turn.
	        this.score += currentRoundScore;
	        
	        this.output.println(this.name + " ended their turn with " + this.score + " points.");

	        return (this.score >= 100);
	    }
	    
	    //we define the getters in the player class
	    public String getName() {
	        return this.name;
	    }
	    
	   
	    public int getScore() {
	        return this.score;
	    }
	    // here we make sure that the answer input is made to upper case, so we wont get invalid inputs when entering a correct but lowercase input
	    
	    public String answer() {
	        return this.scanner.nextLine().replaceAll(" ", "").toUpperCase();
	    }
	    // here continueRolling is defined that we came across in the end of the do while statement
	    
	    public boolean continueRolling() {
	    	
	    	// first we print the question if the player in his or her current turn wants to roll another time after not rolling a 1 (see code above)
	        this.output.println("Do you want to roll more? (Y/N)");
	        
	        // then we ask for an input (y/n) 
	        String continueRolling = this.answer();
	        
	        // you already saw that we made sure to make a lower case Y or N an upper case Y or N to prevent unnecessary invalid inputs
	        
	        //now with this while statement we make sure that if the continueRolling input is not equal to Y and not equal to N, that we ask again for a correct input
	        
	        while (!(continueRolling.equals("Y")) && !(continueRolling.equals("N"))) {
	            this.output.println("Please enter only Y/N:");
	            continueRolling = this.answer();
	        }
	        // so you see that the takeTurn (do while statement) keeps going if the continueRolling statement remains true
	        return continueRolling.equals("Y");
	    }
	}

}
