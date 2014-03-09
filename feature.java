public class feature implements Comparable<feature>{
	public int index;//s
	public String feat;//string feat
	public int count;//how many count the feature have
	
	
	public feature(int i, String f){
		index = i;
		feat = f;
		count = 0;
	}
	
	public void addCount(){
		count++;
	}
	
	public int compareTo(feature other){
		if(this.feat.compareTo(other.feat)==0){
			return 0;//same
		}
		return -1;//not the same
	}
	
	/*
	 * check whether string s is this feat
	 */
	public int compareTo(String s){
		return s.compareTo(this.feat);
	}
}
