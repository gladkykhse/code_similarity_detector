package com.svatoslavgladkih.assignment.service;

import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

@Service
public class FileComparatorServicePythonImpl implements FileComparatorService {

    @Override
    public String checkSimilarity(String filename, String text) {
        try {
            Process pythonProcess = Runtime.getRuntime().exec(
                    new String[]{
                            "python3", "/app/main.py", ("--filename="+filename), ("--text="+text)
                    }
            );
            String resultLine = null;
            StringBuilder resultBuilder = new StringBuilder();
            BufferedReader in = new BufferedReader(new InputStreamReader(pythonProcess.getInputStream()));
            while ((resultLine = in.readLine()) != null) {
                resultBuilder.append(resultLine);
            }
            printLines("error", pythonProcess.getErrorStream());
            return resultBuilder.toString();
        } catch (IOException e) {
            return "Error";
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    private static void printLines(String cmd, InputStream ins) throws Exception {
        String line = null;
        BufferedReader in = new BufferedReader(
                new InputStreamReader(ins));
        while ((line = in.readLine()) != null) {
            System.out.println(cmd + " " + line);
        }
    }
}
