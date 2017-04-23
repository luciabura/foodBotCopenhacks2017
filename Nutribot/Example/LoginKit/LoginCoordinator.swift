//
//  LoginCoordinator.swift
//  LoginKit
//
//  Created by Daniel Lozano Valdés on 3/26/17.
//  Copyright © 2017 CocoaPods. All rights reserved.
//

import Foundation
import ILLoginKit
import Alamofire
import UIKit

class LoginCoordinator: ILLoginKit.LoginCoordinator {

    // MARK: - LoginCoordinator
    enum Sections: Int {
        case headers, body
    }
    
    public var UserIDLoggedIn: String?
    
    public var delegate: ViewControllerProtocol? = nil
    var request: Alamofire.Request? {
        didSet {
            oldValue?.cancel()
            
            headers.removeAll()
            body = nil
            elapsedTime = nil
        }
    }
    var headers: [String: String] = [:]
    var body: String?
    var elapsedTime: TimeInterval?
    var segueIdentifier: String?
    
    static let numberFormatter: NumberFormatter = {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        return formatter
    }()
    
    
    override func start() {
        super.start()
        configureAppearance()
    }

    override func finish() {
        super.finish()
    }

    // MARK: - Setup

    func configureAppearance() {
        // Customize LoginKit. All properties have defaults, only set the ones you want.

        // Customize the look with background & logo images
        backgroundImage = #imageLiteral(resourceName: "mainImage")
        // mainLogoImage =
        // secondaryLogoImage =

        // Change colors
        tintColor = UIColor(red: 52.0/255.0, green: 152.0/255.0, blue: 219.0/255.0, alpha: 1)
        errorTintColor = UIColor(red: 253.0/255.0, green: 227.0/255.0, blue: 167.0/255.0, alpha: 1)

        // Change placeholder & button texts, useful for different marketing style or language.
        loginButtonText = "Sign In"
        signupButtonText = "Create Account"
        facebookButtonText = "Sign Up Now"
        forgotPasswordButtonText = "Forgot password?"
        recoverPasswordButtonText = "Recover"
        namePlaceholder = "Name"
        emailPlaceholder = "E-Mail"
        passwordPlaceholder = "Password!"
        repeatPasswordPlaceholder = "Confirm password!"
    }

    // MARK: - Completion Callbacks

    override func login(email: String, password: String) {
        // Handle login via your API
        print("Login with: email =\(email) password = \(password)")
        self.delegate?.presentNextScreen(isSignup: false)
        let params = ["email": email, "password": password]
        let headers = [
            "Content-Type": "application/json; charset=utf-8"
        ]
        
        self.request = Alamofire.request("https://www.neural-guide.me/foodbot/login", method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers)
        refresh()

    }
    
    

    override func signup(name: String, email: String, password: String) {
        // Handle signup via your API
        print("Signup with: name = \(name) email =\(email) password = \(password)")
        
        let params = ["email": email, "password": password, "name": name]
        let headers = [
            "Content-Type": "application/json; charset=utf-8"
        ]
        self.request = Alamofire.request("https://www.neural-guide.me/foodbot/signup1", method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers)
        self.delegate?.presentNextScreen(isSignup: true)
        refresh()
    }

    override func enterWithFacebook(profile: FacebookProfile) {
        // Handle Facebook login/signup via your API
        print("Login/Signup via Facebook with: FB profile =\(profile)")

    }

    override func recoverPassword(email: String) {
        // Handle password recovery via your API
        print("Recover password with: email =\(email)")
    }

}

extension LoginCoordinator {
    
    func refresh() {
        guard let request = request else {
            return
        }
        
        let start = CACurrentMediaTime()
        
        let requestComplete: (HTTPURLResponse?, Result<String>) -> Void = { response, result in
            let end = CACurrentMediaTime()
            self.elapsedTime = end - start
            
            if let response = response {
                for (field, value) in response.allHeaderFields {
                    self.headers["\(field)"] = "\(value)"
                }
            }
            
            //PRINT RESULT HERE
            
            if let segueIdentifier = self.segueIdentifier {
                switch segueIdentifier {
                case "GET", "POST", "PUT", "DELETE":
                    self.body = result.value
                    print("body ---------\n")
                    print(self.body!)
                case "DOWNLOAD":
                    self.body = self.downloadedBodyString()
                default:
                    break
                }
            }
            
        }
        
        if let request = request as? DataRequest {
            request.responseString { response in
                requestComplete(response.response, response.result)
            }
        } else if let request = request as? DownloadRequest {
            request.responseString { response in
                requestComplete(response.response, response.result)
            }
        }
    }
    
    private func downloadedBodyString() -> String {
        let fileManager = FileManager.default
        let cachesDirectory = fileManager.urls(for: .cachesDirectory, in: .userDomainMask)[0]
        
        do {
            let contents = try fileManager.contentsOfDirectory(
                at: cachesDirectory,
                includingPropertiesForKeys: nil,
                options: .skipsHiddenFiles
            )
            
            if let fileURL = contents.first, let data = try? Data(contentsOf: fileURL) {
                let json = try JSONSerialization.jsonObject(with: data, options: JSONSerialization.ReadingOptions())
                let prettyData = try JSONSerialization.data(withJSONObject: json, options: .prettyPrinted)
                
                if let prettyString = String(data: prettyData, encoding: String.Encoding.utf8) {
                    try fileManager.removeItem(at: fileURL)
                    return prettyString
                }
            }
        } catch {
            // No-op
        }
        
        return ""
    }
}
