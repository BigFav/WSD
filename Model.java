import java.util.*;

public class Model {
	public String word;//the word
	public ArrayList<sentence> validation;//validation set
	public ArrayList<ArrayList<sentence>> training;
	public ModelBasedOnKandNum best;
	
	public int count = 0;
	
	public Model(String w,sentence s){
		word = w;
		validation = new ArrayList();
		training = new ArrayList();
		for(int i = 0;i<s.count;i++){
			//initialize count sentences
			ArrayList<sentence> temp = new ArrayList();
			training.add(temp);
		}
	}
	
	public void addsentence(sentence s){
		if(count%5==1){
			//add to validation set
			validation.add(s);
		}
		else{
			//add to training
			ArrayList<Integer> myvalue = new ArrayList<Integer>(s.value);
			for(Integer t: myvalue){
				ArrayList<sentence> temp = training.get(t);
				temp.add(s);
				training.remove((int)t);//remove from the training set
				training.add(t, temp);//add back
			}
		}
		count++;
	}
	
	public double setkandnum(){
		double [][] table = new double[40][15];
		
		for(int i = 0;i<table.length;i++){
			for(int j = 0;j<table[0].length;j++){
				//k = j+1; num = i+10;
				//create the model
				ArrayList<Integer> counts = new ArrayList();
				for(ArrayList<sentence> s: training){
					counts.add(s.size());
				}
				ModelBasedOnKandNum model = new ModelBasedOnKandNum(j+1,i+10,training,counts);
				//test the model in validation
				double temp = model.runvalidation(validation);
				if(best==null){
					best = model;//initialize the best
				}
				else if(temp>best.score){
					best = model;//update
				}
				
				//check with the best
				
			}
		}
		if(best.tp+best.fp==0){
			return 0;
		}
		else{
			return 1.0*best.tp/(best.tp+best.fp);
		}
	}
}
