import java.util.ArrayList;
import java.util.Comparator;
import java.util.Hashtable;
import java.util.PriorityQueue;
import java.util.Set;

class min implements Comparator{//comparator used for minheap
	public min(){}
	public int compare(Object o1, Object o2){
		myString s1 = (myString) o1;
		myString s2 = (myString) o2;
		return s1.compareTo(s2);
	}
}

public class ModelBasedOnKandNum {
	public ArrayList<Integer> counts;//count(s)
	public ArrayList<Double> probs;//prob(s)
	public Hashtable<String,Integer> mostfrequent;//the most frequently word
	public int k;//k surrounding words
	public int num;//num of most frequently occurred words
	public double threshold;//the threshold
	public Hashtable<Integer, Hashtable<String, feature>> featurecount;
	
	public int tp = 0;
	public int fp = 0;
	public int fn = 0;
	
	/* featurecount:
	 * Integer : s
	 * String: feat; feature: count(f,s)
	 */
	public double score;
	
	public int totalwords;
	
	public ModelBasedOnKandNum(int kk, int nn,ArrayList<ArrayList<sentence>> t,ArrayList<Integer> tempcount){
		k = kk;
		counts = new ArrayList(tempcount);//initialize
		probs = new ArrayList();//initialize
		int sum = 0;
		for(Integer temp:counts){
			sum = sum+temp;
		}
		for(Integer temp: counts){
			probs.add(1.0*temp/sum);//this is prob({s_i})
		}
		num = nn;
		Hashtable<String, Integer> table = new Hashtable<String, Integer>();
		//get a count of the word
		for(ArrayList<sentence> s:t){
			for(sentence ss:s){
				ArrayList<String> words = ss.wordAroundIndex(kk);
				for(String w: words){
					int i;
					if(table.containsKey(w)){
						i = table.get(w);
						i++;
					}
					else{
						i = 1;
					}
					table.put(w, i);
				}
			}
		}
		
		//find out the most frequently words
		Set<String> word = table.keySet();
		PriorityQueue minHeap = new PriorityQueue(num,new min());
		for(String w: word){
			myString temps = new myString(w,table.get(w));
			if(minHeap.size()<num){
				minHeap.add(temps);
			}
			else if(temps.compareTo((myString)minHeap.peek())>0){
				minHeap.poll();
				minHeap.add(temps);
			}
		}
		mostfrequent = new Hashtable();
		while(minHeap.size()>0){
			myString temp = (myString)minHeap.poll();
			mostfrequent.put(temp.value(),temp.count);
		}
		//mostfrequent words finished
		
		//after finding out the most frequently occurred words, we need to figure out count(f, s)
		featurecount = new Hashtable();
		int groupindex = 0;
		for(ArrayList<sentence>s: t){
			//for each group initialize the hashtable first
			Hashtable<String, feature> tempfeature = new Hashtable();
			for(String temps: mostfrequent.keySet()){
				feature f = new feature(groupindex,temps);
				tempfeature.put(temps, f);
			}
			
			for(sentence ss: s){
				//for every sentence in s
				ArrayList<String> groupword = new ArrayList(ss.wordAroundIndex(k));
				for(String wordtemp:groupword){
					if(tempfeature.containsKey(wordtemp)){
						feature tempf = tempfeature.get(wordtemp);
						tempf.addCount();
						tempfeature.put(wordtemp, tempf);//add back
					}
				}
			}
			featurecount.put(groupindex, tempfeature);
			groupindex++;//increment
		}		
	}
	
	public double runvalidation(ArrayList<sentence> v){
		//step1: set up the threshold
		int thresholdcount = 0;
		for(sentence c:v){
			ArrayList<String> word = c.wordAroundIndex(k);//get all the words
			ArrayList<Integer> tempvalue = new ArrayList<Integer>(c.value);
			//find the ones that are in the feature set
			Hashtable<String, Integer> featureInAns = new Hashtable<String, Integer>();
			for(String temp:word){
				if(mostfrequent.containsKey(temp)){
					featureInAns.put(temp, 1);
				}
			}
			Set<Integer> myfeat = featurecount.keySet();
			for(Integer temp: myfeat){
				//check the prob in this category
				//p = p(temp) * p(f|temp) = p(temp) * count(f_j,temp) / count(temp)
				double ptemp = Math.log(probs.get((int)temp));
				int count_temp = counts.get((int)temp);
				ArrayList<Double> countf_temp = new ArrayList();
				for(String s:mostfrequent.keySet()){
					double countf_j = 1.0/1000000000.0;
					if(featureInAns.containsKey(s)){
						countf_j = featurecount.get(temp).get(s).count;//set the count
					}
					countf_temp.add(countf_j);
				}
				if(tempvalue.contains(temp)){
					thresholdcount++;
					double probab = ptemp;
					for(Double countf_j:countf_temp){
						probab = probab+Math.log(countf_j/count_temp);
					}
//					probab = probab/(countf_temp.size()+1);
					this.threshold = this.threshold+Math.exp(probab);
					thresholdcount++;
				}
			}
		}
		this.threshold = this.threshold/thresholdcount;
//		System.out.println(threshold);
		//step2: find the score
		int correct = 0;
		int total = 0;
		for(sentence c: v){
			ArrayList<String> word = c.wordAroundIndex(k);//get all the words
			ArrayList<Integer> tempvalue = new ArrayList<Integer>(c.value);
			//find the ones that are in the feature set
			Hashtable<String, Integer> featureInAns = new Hashtable<String, Integer>();
			for(String temp:word){
				if(mostfrequent.containsKey(temp)){
					featureInAns.put(temp, 1);
				}
			}
			Set<Integer> myfeat = featurecount.keySet();
			for(Integer temp: myfeat){
				double ptemp = Math.log(probs.get((int)temp));
				int count_temp = counts.get((int)temp);
				ArrayList<Double> countf_temp = new ArrayList();
				for(String s:mostfrequent.keySet()){
					double countf_j = 1.0/1000000000.0;
					if(featureInAns.containsKey(s)){
						countf_j = featurecount.get(temp).get(s).count;//set the count
					}
					ptemp = ptemp + Math.log(countf_j/count_temp);
					countf_temp.add(countf_j);
				}
//				ptemp = ptemp/(countf_temp.size()+1);
				ptemp = Math.exp(ptemp);
				if(ptemp>this.threshold){
					//we predict true here
					if(c.value.contains(temp)){
						tp++;
						correct++;
					}
					else{
						fp++;
					}
				}
				else{
					if(!c.value.contains(temp)){
						correct++;
					}else{
						fn++;
					}
				}
				total++;
			}
		}
		//step3: return the score

		score = 1.0*correct/(1.0*total);
		return score;
	}
	
	public ArrayList<Integer> predict(sentence c){
		ArrayList<Integer> result = new ArrayList<Integer>();
		for(int i = 0;i<probs.size();i++){
			result.add(0);
		}
		boolean set = false;
		ArrayList<String> word = c.wordAroundIndex(k);//get all the words
		Hashtable<String, Integer> featureInAns = new Hashtable<String, Integer>();
		for(String temp:word){
			if(mostfrequent.containsKey(temp)){
				featureInAns.put(temp, 1);
			}
		}
		Set<Integer> myfeat = featurecount.keySet();
		for(Integer temp: myfeat){
			double ptemp = probs.get((int)temp);
			int count_temp = counts.get((int)temp);
			ArrayList<Double> countf_temp = new ArrayList();
			for(String s:mostfrequent.keySet()){
				double countf_j = 1.0/1000000000.0;//make it a really small number
				if(featureInAns.containsKey(s)){
					countf_j = featurecount.get(temp).get(s).count;//set the count
				}
				ptemp = ptemp *countf_j/count_temp;
				countf_temp.add(countf_j);
			}
//			ptemp = ptemp/(countf_temp.size()+1);
			if(ptemp>this.threshold){
				//we predict true here
				set = true;
				result.remove((int)temp);
				result.add((int)temp,1);
			}
		}
		if(set){
			result.add(0, 1);
		}
		else{
			result.add(0, 0);
		}
		return result;
	}
}
