//
//  UserObject.swift
//  LoginKit
//
//  Created by Andrei Ionescu on 23/04/2017.
//  Copyright © 2017 CocoaPods. All rights reserved.
//

import Foundation

public class UserObject: NSObject {
    
    var Name: String = ""
    var target: String = ""
    var id: String = ""
    var email: String = ""
    var gender: String = ""
    var activityLevel: Int = 0
    var listOfIntolerances: [String] = []
    var dateOfBirth: String = ""
    var finishedSignup: Bool = false
    
    public override init() {
    }
    
    public func isItFinished() -> Bool {
        return true
    }
    
}
