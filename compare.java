import java.io.*;
import java.util.*;
import java.util.zip.*;


public class compare{
static ClassLoader classLoader;
static InputStream inputStream;
static BufferedReader reader;
static List<String> wordList;
static String line;
static String[] words;
static Set<String> wordSet;
static InputStream fileStream;
static InputStream gzipStream;
static Reader decoder;
static BufferedReader buffered;
static String tmp;

  public static void main(String[] args){
    System.out.println(args[0]);
    System.out.println(args[1]);

    final File folder = new File(args[0]);
    listFilesForFolder(folder, args[1]);
  }

  public static void listFilesForFolder(final File folder, String newFile) {
    for (final File fileEntry : folder.listFiles()) {
        if (fileEntry.isDirectory()) {
            listFilesForFolder(fileEntry, newFile);
        } else
        try{
          //FASTA FILES
          classLoader = ClassLoader.getSystemClassLoader();
          inputStream = classLoader.getResourceAsStream(newFile);
          reader = new BufferedReader(new InputStreamReader(inputStream));
          wordList = new LinkedList<String>();
          line = null;
          while ((line = reader.readLine()) != null) {
            words = line.toLowerCase().split("\\W+");
            wordList.addAll(Arrays.asList(words));
          }
          wordSet = new HashSet<String>(wordList.size());
          wordSet.addAll(wordList);
          //Library Files
          fileStream = new FileInputStream(fileEntry.getName());
          gzipStream = new GZIPInputStream(fileStream);
          decoder = new InputStreamReader(gzipStream, "UTF-8");
          buffered = new BufferedReader(decoder);
          tmp = null;
          while ((tmp = buffered.readLine()) != null) {
            if(wordSet.contains(tmp)){
              System.out.print("true");
            }
          }
        }
      catch(IOException e){
        e.printStackTrace();
      }
    }
  }
}
