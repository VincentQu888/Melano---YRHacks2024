package com.example.Melano;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class AnchorController {

    @GetMapping("/")
    String index(Model model){
        return "index";
    }

}
