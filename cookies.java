提取cookie：

JSR223 PostProcessor

//import java.io.BufferedReader;

//import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;
import java.io.*;

String responseheaders = prev.getResponseHeaders();
BufferedReader buffer_reader = new BufferedReader(new StringReader(responseheaders));
List<String> response_origin_list = new ArrayList<>();

for(String line = buffer_reader.readLine(); line != null;line = buffer_reader.readLine()){
response_origin_list.add(line);
}

int origin_size = response_origin_list.size();
String response_cookie = "";

for(i=0;i<origin_size;i++){
String[] cookie_item = response_origin_list[i].split(":");
if(cookie_item[0].equals("Set-Cookie"))
response_cookie += cookie_item[1].trim()+";";
}

String response_cookie_final = response_cookie.substring(0,response_cookie.length()-1);

vars.put("responsecookie",response_cookie_final);



FileWriter fstream = new FileWriter("D:\\workspace\\项目\\可信评估\\cookie.txt",true);
BufferedWriter out =new BufferedWriter(fstream);
out.write(vars.get("responsecookie"));
out.close();
fstream.close();
二、设置全局cookie

BeanShell PreProcessor

string a=bsh.args[0];
print(a);
${__setProperty(cookies,${responsecookie},)}
