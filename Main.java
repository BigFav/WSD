import java.util.*;
import java.util.regex.*;
import java.io.*;
import snowball.SnowballStemmer;


public class Main {
	public static void main(String [] args) throws Throwable{
//		Hashtable<String, ArrayList<sentence>> validation = new Hashtable();
		
//		stemming("./data/Training Data.data",validation,5,10);
		implementModels("./data/Training Data.data","./data/Test Data.data");
		System.out.println("Finished");
	}
	
	/*
	 * filename: the filename of the training data
	 * validation: <key, value> key: the label of the line
	 * 							value: the validaion set
	 * k: # of surrounding words
	 * num: the num of most frequent word
	 */
	public static void stemming(String filename, Hashtable<String, ArrayList<sentence>> validation,int k, int num)throws Throwable{
		
		Scanner s = new Scanner(new File(filename));
		String label = null;//define the label as empty
		int count = 0;
		Hashtable<String, Integer> global = new Hashtable<String, Integer>();
		Hashtable<String, Hashtable<String,Integer>> features = new Hashtable();
		Hashtable<String, ArrayList<ArrayList<String>>> table = new Hashtable();
		while(s.hasNext()){
			String line = s.nextLine();
			sentence new_sentence = new sentence(line);//generate the sentence
			if(label==null){
				label = new_sentence.word;
			}
			if(label.compareTo(new_sentence.word)!=0){
				//change of word
				Set<String> word = global.keySet();
				PriorityQueue minHeap = new PriorityQueue(num,new min());
				for(String w: word){
					myString temps = new myString(w,global.get(w));
					if(minHeap.size()<num){
						minHeap.add(temps);
					}
					else if(temps.compareTo((myString)minHeap.peek())>0){
						minHeap.poll();
						minHeap.add(temps);
					}
				}
				
				Hashtable<String, Integer> tempfeature = new Hashtable();
				while(minHeap.size()>0){
					myString temp = (myString)minHeap.poll();
					tempfeature.put(temp.value(),temp.count);
				}
				features.put(label, tempfeature);
				
				label = new_sentence.word;
				count = 0;
			}
			if(count % 5==1){
				//validation set
				if(validation.containsKey(new_sentence.word)){
					ArrayList<sentence> temp = validation.get(new_sentence.word);
					temp.add(new_sentence);
					validation.put(new_sentence.word, temp);
				}
				else{
					ArrayList<sentence> temp = new ArrayList<sentence>();
					temp.add(new_sentence);
					validation.put(new_sentence.word, temp);
				}
			}
			else{
				//trainning data
				ArrayList<String> temp = new_sentence.wordAroundIndex(k);
				for(String t: temp){
					if(global.containsKey(t)){
						int v = global.get(t);
						v++;
						global.put(t,v);
					}
					else{
						global.put(t,1);
					}
				}
				
				ArrayList<Integer> tempvalue = new ArrayList(new_sentence.value);
				if(!table.containsKey(label)){
					//initialize
					ArrayList<ArrayList<String>> tempvaluearray = new ArrayList();
					for(int i = 0;i<new_sentence.count;i++){
						tempvaluearray.add(new ArrayList<String>());//add count arrayList into the temp...
					}
					table.put(new_sentence.word, tempvaluearray);
				}
				for(Integer tempv:tempvalue){
					
				}
			}
		}
		s.close();
	}

	public static void implementModels(String filename,String test) throws Throwable{
		Scanner s = new Scanner(new File(filename));
		
		Hashtable<String, Model> myModel = new Hashtable<String, Model> ();
		
		while(s.hasNext()){
			String line = s.nextLine();
			sentence tempsentence = new sentence(line);
			if(myModel.containsKey(tempsentence.word)){
				//we have the model already
				//add the model into the hashtable
				Model m = myModel.get(tempsentence.word);
				m.addsentence(tempsentence);
				myModel.put(tempsentence.word, m);
			}
			else{
				//create the new model
				Model m = new Model(tempsentence.word, tempsentence);
				m.addsentence(tempsentence);
				//add to the hashtable
				myModel.put(tempsentence.word, m);
			}
		}
		s.close();
		//finish reading from the file
		Set<String> myset = myModel.keySet();
		double sum = 0.0;
		for(String t:myset){
			Model m = myModel.get(t);
			sum = sum+m.setkandnum();//generate the best k and num using training set.
		}
		sum = sum/myset.size();
//		System.out.println("Precision:" + sum);
		s = new Scanner(new File(test));
		ArrayList<ArrayList<Integer>> re = new ArrayList();
		while(s.hasNext()){
			String line = s.nextLine();
			sentence temp = new sentence(line);
			Model m = myModel.get(temp.word);
			re.add(m.best.predict(temp));
		}
		s.close();
		String out = "./data/prediction";
		FileWriter fstream = new FileWriter(out);
		BufferedWriter output = new BufferedWriter(fstream);
		for(ArrayList<Integer> t:re){
			for(Integer tt: t){
				output.write(tt+"\n");
			}
		}
		output.close();
	}
}
