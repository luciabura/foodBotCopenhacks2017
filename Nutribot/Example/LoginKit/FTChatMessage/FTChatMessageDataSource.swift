//
//  FTChatMessageDataSource.swift
//  FTChatMessage
//
//  Created by liufengting on 16/8/19.
//  Copyright © 2016年 liufengting <https://github.com/liufengting>. All rights reserved.
//

import UIKit

@objc protocol FTChatMessageDataSource : NSObjectProtocol {
    
    func ftChatMessageMessageArray() -> [FTChatMessageModel]
    
}
