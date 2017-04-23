//
//  ViewController.swift
//  LoginKit
//
//  Created by Daniel Lozano on 12/12/2016.
//  Copyright (c) 2016 Daniel Lozano. All rights reserved.
//

import UIKit
import ILLoginKit
import Alamofire


protocol ViewControllerProtocol {
    func presentNextScreen(isSignup: Bool);
}


class ViewController: UIViewController {

    lazy var loginCoordinator: LoginCoordinator = {
        var coordinator: LoginCoordinator = LoginCoordinator(rootViewController: self)
        coordinator.delegate = self
        return coordinator
    }()

    override func viewDidLoad() {
        super.viewDidLoad()
        loginCoordinator.start()

    }

    override func viewDidAppear(_ animated: Bool) {
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    

}

extension ViewController: ViewControllerProtocol {
    
    func presentNextScreen(isSignup: Bool) {
        loginCoordinator.finish()
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let controller = storyboard.instantiateViewController(withIdentifier: "chatViewController") as! ChatTableViewController
        controller.isSignupChat = isSignup
        self.navigationController?.pushViewController(controller, animated: true)
        self.navigationController?.popViewController(animated: false)


    }

    
}

