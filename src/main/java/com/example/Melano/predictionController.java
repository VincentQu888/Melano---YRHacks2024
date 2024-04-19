package com.example.Melano;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.*;

import javax.imageio.ImageIO;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import jakarta.servlet.http.HttpServletRequest;

@Controller
public class predictionController {
    
    @PostMapping("/upload")
    private String upload(@RequestParam("img") MultipartFile img, RedirectAttributes redirectAttributes)throws IOException, FileNotFoundException, InterruptedException{
        FileOutputStream fileOutputStream = new FileOutputStream("uploaded_img.jpg");
        fileOutputStream.write(img.getBytes());
        fileOutputStream.close();


        long startTime = System.nanoTime();


        Process process = Runtime.getRuntime().exec("python prediction_model.py");
        process.waitFor();

        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String line, output = "";
        while((line = reader.readLine()) != null){
            output = line;
        }


        long endTime = System.nanoTime();
        long elapsedTime = (endTime - startTime)/1000000;


        double prediction = Double.parseDouble(output);
        if(prediction > 0.75 && prediction != 1.0){
            redirectAttributes.addFlashAttribute("prediction", "Likely has melanoma");
        }else if(prediction > 0.6 && prediction != 1.0){
            redirectAttributes.addFlashAttribute("prediction", "May have melanoma");
        }else{
            redirectAttributes.addFlashAttribute("prediction", "Unlikely to have melanoma");
        }

        redirectAttributes.addFlashAttribute("prob", prediction);
        redirectAttributes.addFlashAttribute("runtime", elapsedTime);
        return "redirect:result";
    }
}
