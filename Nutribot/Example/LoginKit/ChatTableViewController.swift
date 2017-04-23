import UIKit
import FTIndicator
import MBProgressHUD
import ApiAI
import Alamofire


class ChatTableViewController: FTChatMessageTableViewController,FTChatMessageAccessoryViewDelegate,FTChatMessageAccessoryViewDataSource,FTChatMessageRecorderViewDelegate,UIImagePickerControllerDelegate,UINavigationControllerDelegate{
    
    
    
    
    
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
    
    
    

    let sender1 = FTChatMessageUserModel.init(id: "1", name: "Bot", icon_url: "https://www.charusat.ac.in/wp-content/uploads/2014/05/user.jpg", extra_data: nil, isSelf: false)
    
    var isSignupChat: Bool = true
    var textForAPI: String?
    var userObject: UserObject!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.navigationItem.setRightBarButton(UIBarButtonItem.init(barButtonSystemItem: UIBarButtonSystemItem.add, target: self, action: #selector(self.addNewIncomingMessage)), animated: true)
        
        messageRecordView.recorderDelegate = self
        messageAccessoryView.setupWithDataSource(self , accessoryViewDelegate : self)
        
        chatMessageDataArray = self.loadDefaultMessages()
        
        self.userObject = UserObject()

    }

    //MARK: - addNewIncomingMessage
    
    func addNewIncomingMessage() {
        
        let message8 = FTChatMessageModel(data: "New Message added, try something else.", time: "4.12 22:42", from: sender1, type: .text)
        self.addNewMessage(message8)

    }

    func loadDefaultMessages() -> [FTChatMessageModel] {
        

        if !self.isSignupChat {
            let message1 = FTChatMessageModel(data: "Welcome! What would you like to eat today?", time: "4.12 21:09:50", from: sender1, type: .text)
            
            let array = [message1]
            
            return array;
        }
        else {
        let message1 = FTChatMessageModel(data: "Hi! Thank you for registering. I have to ask you a couple more questions in order to present you the best recipes! Ready?", time: "4.12 21:09:50", from: sender1, type: .text)

        let message2 = FTChatMessageModel(data: "So, can you please tell me your date of birth?", time: "4.12 21:09:50", from: sender1, type: .text)
            
            let array = [message1, message2]
            
            return array;
        }


        
        
        
    }
    
    
    func getAccessoryItemTitleArray() -> [String] {
        return ["Alarm","Camera","Contacts","Mail","Messages","Music","Phone","Photos","Settings","VideoChat","Videos","Weather"]
    }

    
    //MARK: - FTChatMessageAccessoryViewDataSource
    
    func ftChatMessageAccessoryViewModelArray() -> [FTChatMessageAccessoryViewModel] {
        var array : [FTChatMessageAccessoryViewModel] = []
        let titleArray = self.getAccessoryItemTitleArray()
        for i in 0...titleArray.count-1 {
            let string = titleArray[i]
            array.append(FTChatMessageAccessoryViewModel.init(title: string, iconImage: UIImage(named: string)!))
        }
        return array
    }

    //MARK: - FTChatMessageAccessoryViewDelegate
    
    func ftChatMessageAccessoryViewDidTappedOnItemAtIndex(_ index: NSInteger) {
        
        if index == 0 {
            
            let imagePicker : UIImagePickerController = UIImagePickerController()
            imagePicker.sourceType = .photoLibrary
            imagePicker.delegate = self
            self.present(imagePicker, animated: true, completion: { 
                
            })
        }else{
            let string = "I just tapped at accessory view at index : \(index)"
            
            print(string)
            
            //        FTIndicator.showInfo(withMessage: string)
            
            let message2 = FTChatMessageModel(data: string, time: "4.12 21:09:51", from: sender2, type: .text)
            
            self.addNewMessage(message2)
        }
    }
    
    override func ft_chatMessageInputViewShouldDoneWithText(_ textString: String) {
        super.ft_chatMessageInputViewShouldDoneWithText(textString)
        
        self.textForAPI = textString
        print("stuuuuuuuuufffffff")
        self.sendtextToAPIAI()
        //NEED TO INTERPRET THE MESSAGE HERE
        
    }
    
    //MARK: - FTChatMessageRecorderViewDelegate
    
    func ft_chatMessageRecordViewDidStartRecording(){
        print("Start recording...")
        FTIndicator.showProgressWithmessage("Recording...")
    }
    func ft_chatMessageRecordViewDidCancelRecording(){
        print("Recording canceled.")
        FTIndicator.dismissProgress()
    }
    func ft_chatMessageRecordViewDidStopRecording(_ duriation: TimeInterval, file: Data?){
        print("Recording ended!")
        FTIndicator.showSuccess(withMessage: "Record done.")
        
        let message2 = FTChatMessageModel(data: "", time: "4.12 21:09:51", from: sender2, type: .audio)

        self.addNewMessage(message2)
        
    }
    
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        
        picker.dismiss(animated: true) {
            
            let image : UIImage = info[UIImagePickerControllerOriginalImage] as! UIImage
            let message2 = FTChatMessageImageModel(data: "", time: "4.12 21:09:51", from: self.sender2, type: .image)
            message2.image = image;
            self.addNewMessage(message2)
        }
    }
    
    func saveImageToDisk(image: UIImage) -> String {
        
        return ""
    }
    
    
    func sendtextToAPIAI() {
        let hud = MBProgressHUD.showAdded(to: self.view.window!, animated: true)
        
//        self.textField?.resignFirstResponder()
        
        let request = ApiAI.shared().textRequest()
        
        if let text = self.textForAPI {
            request?.query = [text]
        } else {
            request?.query = [""]
        }
        
        request?.setMappedCompletionBlockSuccess({ (request, response) in
            let response = response as! AIResponse
            if response.result.action == "money" {
                if let parameters = response.result.parameters as? [String: AIResponseParameter]{
                    let amount = parameters["amout"]!.stringValue
                    let currency = parameters["currency"]!.stringValue
                    let date = parameters["date"]!.dateValue
                    
                    print("Spended \(amount) of \(currency) on \(date)")
                }
            }
        }, failure: { (request, error) in
            // TODO: handle error
        })
        
        request?.setCompletionBlockSuccess({[unowned self] (request, response) -> Void in
            
            //print(response as! String)
            let theResponse: AnyObject = response as AnyObject
            var apiAIResponse: AIResponse = AIResponse.init(response: response)

            print(theResponse.description)
            let message = FTChatMessageModel(data: apiAIResponse.result.fulfillment.speech, time: "4.12 21:09:50", from: self.sender1, type: .text)
            if self.isSignupChat {
            self.addNewMessage(message)
            }
            
            //here i pass the data to obj
            var paramsDict: Dictionary = apiAIResponse.result.parameters
            self.userObject.dateOfBirth = "1995-07-15"
            self.userObject.activityLevel = 4
            self.userObject.id = "1"
            self.userObject.gender = "M"
            self.userObject.listOfIntolerances = ["gluten"]
            
            
            hud.hide(animated: true)
            }, failure: { (request, error) -> Void in
                hud.hide(animated: true)
        });
        
        
        if isSignupChat {
            
        
        
        
        if  self.userObject.isItFinished() {
            
            let params = [
                "userID" : self.userObject.id,
                "gender" : self.userObject.gender,
                "Activity_level" : self.userObject.activityLevel,
                "date_of_birth" : self.userObject.dateOfBirth,
                "target" : self.userObject.target,
                "intolerances" : ["gluten"],
                "preferences" : ["vegetarian"],
                "diseases" : ""
            ] as [String : Any]
            
            self.request = Alamofire.request("https://www.neural-guide.me/signup2", method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers)
            self.refresh()
        }
            
        } else {
            
            if self.textForAPI == "What can I eat today?" {
                let params = ["":""]
                self.request = Alamofire.request("https://www.neural-guide.me/signup2", method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers)
                self.refresh()
                let message = FTChatMessageModel(data: "Sure. Here is a list of options:", time: "4.12 21:09:50", from: self.sender1, type: .text)
                self.addNewMessage(message)
                
                let message3 = FTChatMessageModel(data: "Mac and cheese", time: "4.12 21:09:50", from: self.sender1, type: .text)

                let message4 = FTChatMessageModel(data: "Pancakes with bananas", time: "4.12 21:09:50", from: self.sender1, type: .text)

                let message5 = FTChatMessageModel(data: "Tomato and Basil Soup", time: "4.12 21:09:50", from: self.sender1, type: .text)
                
                self.addNewMessage(message3)
                self.addNewMessage(message4)
                self.addNewMessage(message5)




            } else if self.textForAPI == "What can I eat this morning?"{
                let params = ["":""]
                self.request = Alamofire.request("https://www.neural-guide.me/signup2", method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers)
                self.refresh()
                let message = FTChatMessageModel(data: "Sure. Mac and cheese sounds like a good idea!", time: "4.12 21:09:50", from: self.sender1, type: .text)
                self.addNewMessage(message)
            } else if self.textForAPI == "Can you reccomend me something vegetarian?"{
                let params = ["":""]
                self.request = Alamofire.request("https://www.neural-guide.me/signup2", method: .post, parameters: params, encoding: JSONEncoding.default, headers: headers)
                self.refresh()
                let message = FTChatMessageModel(data: "Hmmmm.....I think some an omlete with cheese and tomatoes is suitable for you at this hour.", time: "4.12 11:09:50", from: self.sender1, type: .text)
                self.addNewMessage(message)
            }
            
            
        }
        
        ApiAI.shared().enqueue(request)
    }
    
    func convertToDictionary(text: String) -> [String: Any]? {
        if let data = text.data(using: .utf8) {
            do {
                return try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
            } catch {
                print(error.localizedDescription)
            }
        }
        return nil
    }
    

}


extension ChatTableViewController {
    
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
            if let jsonResult = result as? Dictionary<String, AnyObject> {
                // do whatever with jsonResult
            }
            
            
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
