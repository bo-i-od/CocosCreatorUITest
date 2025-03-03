import { _decorator, Component, Node, screen, Camera } from 'cc';
import { Locate } from './Locate';
import { UIData } from './UIData';
const { ccclass, property } = _decorator;

@ccclass
export default class WSClient extends Component {
    private socket: WebSocket = null;
    private reconnectTimer: number = 0;
    private baseDelay = 500;
    private cameraDefault: Camera;
    private rpcHandlers: { [key: string]: (params: any) => any} = {}; // RPC 方法注册表
    public idToNode: Map<string, Node> = new Map();
    @property({ type: String})
    public port:string = "5101";
    // 注册 RPC 方法
    registerRpcHandler(methodName: string, callback: (params: any) => any) {
        this.rpcHandlers[methodName] = callback;
    }


    onLoad() {
        this.addRpcMethods();
        this.startConnection();
        this.transmitConsole();

    }

    private addRpcMethods(){
        this.registerRpcHandler("getScreenSize", this.getScreenSize.bind(this));
        this.registerRpcHandler("getPosition", this.getPosition.bind(this));
        this.registerRpcHandler("getPositionByID", this.getPositionByID.bind(this));
        this.registerRpcHandler("getSize", this.getSize.bind(this));
        this.registerRpcHandler("getSizeByID", this.getSizeByID.bind(this));
        this.registerRpcHandler("getText", this.getText.bind(this));
        this.registerRpcHandler("getTextByID", this.getTextByID.bind(this));
        this.registerRpcHandler("setText", this.setText.bind(this));
        this.registerRpcHandler("setTextByID", this.setTextByID.bind(this));
        this.registerRpcHandler("getSpriteName", this.getSpriteName.bind(this));
        this.registerRpcHandler("getSpriteNameByID", this.getSpriteNameByID.bind(this));
        this.registerRpcHandler("getProgress", this.getProgress.bind(this));
        this.registerRpcHandler("getProgressByID", this.getProgressByID.bind(this));
        this.registerRpcHandler("getToggleIsChecked", this.getToggleIsChecked.bind(this));
        this.registerRpcHandler("getToggleIsCheckedByID", this.getToggleIsCheckedByID.bind(this));
        this.registerRpcHandler("getName", this.getName.bind(this));
        this.registerRpcHandler("getNameByID", this.getNameByID.bind(this));
        this.registerRpcHandler("getID", this.getID.bind(this));
        this.registerRpcHandler("getIDByID", this.getIDByID.bind(this));
        this.registerRpcHandler("getParentID", this.getParentID.bind(this));
        this.registerRpcHandler("getParentIDByID", this.getParentIDByID.bind(this));
        this.registerRpcHandler("command", this.command.bind(this));
        this.registerRpcHandler("customCommand", this.customCommand.bind(this));
    }

    // 获取分辨率
    private getScreenSize() {
        return [screen.resolution.width, screen.resolution.height];

    }

    private getPosition(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            let camera: Camera = this.cameraDefault;
            if ("locator_camera" in elementData)
            {
                let cameraNodeArray: Node[]  = Locate.locateNodeArray(elementData.locator_camera);
                const component = cameraNodeArray[0].getComponent(Camera);
                if(component){
                    camera = component;
                }
            }
            let anchorPoint: number[] = [0.5, 0.5];
            if("anchor_point" in elementData){
                anchorPoint = elementData.anchor_point;
            }
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const positionArray: number[][] = UIData.getPositionArray(targetNodeArray, camera);
            const sizeArray: number[][] = UIData.getPositionArray(targetNodeArray, camera);
            const correctedPositionArray = UIData.correctPosition(positionArray, sizeArray, anchorPoint)
            res.push(correctedPositionArray);
            cur += 1;
        }
        return res;
    }

    private getPositionByID(params){

        const idArray: string[] = params[0];
        const offspringPath: string = params[1];
        const anchorPoint: number[] = params[2];
        const locatorCamera = params[3];
        let cur:number = 0;
        let res = [];
        while(cur < idArray.length){
            let camera: Camera = this.cameraDefault;
            if (locatorCamera != "")
            {
                let cameraNodeArray: Node[]  = Locate.locateNodeArray(locatorCamera);
                const component = cameraNodeArray[0].getComponent(Camera);
                if(component){
                    camera = component;
                }
            }
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            const positionArray: number[][] = UIData.getPositionArray(targetNodeArray, camera);
            const sizeArray: number[][] = UIData.getPositionArray(targetNodeArray, camera);
            const correctedPositionArray = UIData.correctPosition(positionArray, sizeArray, anchorPoint)
            res.push(correctedPositionArray);
            cur += 1;
        }
        return res;
    }

    private getSize(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const sizeArray: number[][] = UIData.getSizeArray(targetNodeArray);
            res.push(sizeArray);
            cur += 1;
        }
        return res;
    }

    private getSizeByID(params){
        const idArray: string[] = params[0];
        const offspringPath: string = params[1];
        let cur:number = 0;
        let res = [];
        while(cur < idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            const sizeArray: number[][] = UIData.getSizeArray(targetNodeArray);
            res.push(sizeArray);
            cur += 1;
        }
        return res;
    }

    private getText(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const textArray: string[] = UIData.getTextArray(targetNodeArray);
            res.push(textArray);
            cur += 1;
        }
        return res;
    }

    private getTextByID(params){
        const idArray: string[] = params[0];
        const offspringPath: string = params[1];
        let cur:number = 0;
        let res = [];
        while(cur < idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            const textArray: string[] = UIData.getTextArray(targetNodeArray);
            res.push(textArray);
            cur += 1;
        }
        return res;
    }

    private setText(params){
        const elementDataArray = params[0];
        const text: string = params[1];
        let cur:number = 0;
        let elementData;
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            UIData.setTextArray(targetNodeArray, text);
            cur += 1;
        }
        return null;
    }

    private setTextByID(params){
        const idArray: string[] = params[0];
        const offspringPath: string = params[1];
        const text: string = params[2];
        let cur:number = 0;
        while(cur < idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            UIData.setTextArray(targetNodeArray, text);
            cur += 1;
        }
        return null;
    }

    private getSpriteName(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const spriteNameArray: string[] = UIData.getSpriteNameArray(targetNodeArray);
            res.push(spriteNameArray);
            cur += 1;
        }
        return res;
    }

    private getSpriteNameByID(params){
        const idArray: string[] = params[0];
        const offspringPath: string = params[1];
        let cur:number = 0;
        let res = [];
        while(cur < idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            const spriteNameArray: string[] = UIData.getSpriteNameArray(targetNodeArray);
            res.push(spriteNameArray);
            cur += 1;
        }
        return res;
    }

    private getProgress(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const progressArray: number[] = UIData.getProgressArray(targetNodeArray);
            res.push(progressArray);
            cur += 1;
        }
        return res;
    }

    private getProgressByID(params){
        const idArray: string[] = params[0];
        const offspringPath: string = params[1];
        let cur:number = 0;
        let res = [];
        while(cur < idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            const progressArray: number[] = UIData.getProgressArray(targetNodeArray);
            res.push(progressArray);
            cur += 1;
        }
        return res;
    }

    private getToggleIsChecked(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const toggleIsCheckedArray: boolean[] = UIData.getToggleIsCheckedArray(targetNodeArray);
            res.push(toggleIsCheckedArray);
            cur += 1;
        }
        return res;
    }

    private getToggleIsCheckedByID(params){
        const idArray: string[] = params[0];
        const offspringPath: string = params[1];
        let cur:number = 0;
        let res = [];
        while(cur < idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            const toggleIsCheckedArray: boolean[] = UIData.getToggleIsCheckedArray(targetNodeArray);
            res.push(toggleIsCheckedArray);
            cur += 1;
        }
        return res;
    }

    private getName(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const nameArray: string[] = UIData.getNameArray(targetNodeArray);
            res.push(nameArray);
            cur += 1;
        }
        return res;
    }

    private getNameByID(params){
        const idArray: string[] = params[0];
        const offspringPath: string = params[1];
        let cur:number = 0;
        let res = [];
        while(cur <  idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            const nameArray: string[] = UIData.getNameArray(targetNodeArray);
            res.push(nameArray);
            cur += 1;
        }
        return res;
    }

    private getID(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const idArray: string[] = UIData.getIDArray(targetNodeArray, this.idToNode);
            res.push(idArray);
            cur += 1;
        }
        return res;
    }

    private getIDByID(params){
        const idArray: string[] = params[0];
        let cur:number = 0;
        const offspringPath: string = params[1].toString();
        let res = [];
        while(cur < idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            res.push(UIData.getIDArray(targetNodeArray, this.idToNode));
            cur += 1;
        }
        return res;
    }

    private getParentID(params){
        const elementDataArray = params[0];
        let cur:number = 0;
        let elementData;
        let res = [];
        while(cur < elementDataArray.length){
            elementData = elementDataArray[cur];
            const targetNodeArray: Node[] = Locate.locateNodeArray(elementData.locator);
            const parentNodeArray: Node[] = Locate.getParentNodeArray(targetNodeArray);
            res.push(UIData.getIDArray(parentNodeArray, this.idToNode));
            cur += 1;
        }
        return res;
    }

    private getParentIDByID(params){
        const idArray: string[] = params[0];
        let cur:number = 0;
        const offspringPath: string = params[1].toString();
        let res = [];
        while(cur < idArray.length){
            const id: string = idArray[cur];
            const targetNodeArray: Node[] = Locate.getNodeArrayByID(id, offspringPath, this.idToNode);
            const parentNodeArray = Locate.getParentNodeArray(targetNodeArray);
            res.push(UIData.getIDArray(parentNodeArray, this.idToNode));
            cur += 1;
        }
        return res;
    }

    private command(params){
        let cur = 0;
        const cmdArray = params[0];
        while (cur < cmdArray.length)
        {
            this.commandOnce(cmdArray[cur]);
            cur += 1;
        }
        return null;
    }

    private commandOnce(cmd: string){


    }

    private customCommand(params){
        let cur = 0;
        const cmdArray = params[0];
        while (cur < cmdArray.length)
        {
            this.customCommandOnce(cmdArray[cur]);
            cur += 1;
        }
        return null;
    }

    private customCommandOnce(cmd: string){
        const cmdSplits: string[] = cmd.split(' ');
        if(cmdSplits[0] === "setCamera"){
            let locatorCamera: string = cmd.split(' ', 2)[1];
            let cameraNodeArray: Node[]  = Locate.locateNodeArray(locatorCamera);
            if(cameraNodeArray.length == 0){
                return;
            }
            const component = cameraNodeArray[0].getComponent(Camera);
            if(!component){
                return;
            }
            this.cameraDefault = component;
        }
    }

    startConnection() {
        this.cleanup();
        this.socket = new WebSocket( `ws://localhost:${this.port}`);
        this.socket.onopen = () => {
            // 每次连接后清空uuid映射map
            this.idToNode.clear();
            // this.scheduleHeartbeat();
            // this.socket.send("<----TypeScript->Python---->已连接");
        };

        this.socket.onmessage = (msg) => {
            let response = this.handleMessage(msg);
            this.socket.send(response);
        };

        this.socket.onclose = (ev) => {
            this.handleReconnect();
        };

        this.socket.onerror = (err) => {
            console.log("WebSocket 连接失败，正在重试……");
            this.handleReconnect();
        };
    }

    private handleMessage(msg){
        let method: string;
        let idAction: number;
        let params = {};
        let response: string;
        try {
            const data = JSON.parse(msg.data);
            method = data.method;
            idAction = data.id;
            params = data.params || {};
        } catch (err) {
            console.log("Received non-JSON message:", msg.data);
            response = this.formatResponseError(idAction, err);
            return response;
        }

        // 检查方法是否存在
        if (!this.rpcHandlers.hasOwnProperty(method)) {
            response = this.formatResponseError(idAction, `Method '${method}' not found`);
            return response;
        }

        let result = null;
        try{
            result = this.rpcHandlers[method](params);
        }
        catch(err){
            console.log(err);
            response = this.formatResponseError(idAction, err);
            return response;
        }
        response = this.formatResponse(idAction, result);
        return response;
    }


    private scheduleHeartbeat() {
        this.schedule(() => {
            if (this.socket.readyState === WebSocket.OPEN) {
                this.socket.send("PING");
            }
        }, 10);
    }

    private handleReconnect() {
        const delay = this.baseDelay * 1;
        this.reconnectTimer = setTimeout(() => {
            this.startConnection();
        }, delay);
    }

    private cleanup() {
        if (this.socket) {
            this.socket.close();
            this.unscheduleAllCallbacks();
            clearTimeout(this.reconnectTimer);
        }
    }


    // 格式化消息
    private formatMessage(idAction, msg){
        const data = {
            jsonrpc: "2.0",
            id: idAction,
            msg: msg,
        };
        return JSON.stringify(data);
    }

    private formatResponse(idAction, res){
        const data = {
            jsonrpc: "2.0",
            id: idAction,
            result: res,
        };
        return JSON.stringify(data);
    }

    private formatResponseError(idAction, err){

        const data = {
            jsonrpc: "2.0",
            id: idAction,
            error: this.getErrorMessage(err),
        };
        return JSON.stringify(data);
    }

    private getErrorMessage(err: unknown): string {
        if (err instanceof Error) {
          return err.message; // 提取 Error 对象的 message
        } else if (typeof err === "string") {
          return err; // 直接使用字符串
        } else {
          return String(err); // 处理数字、对象等
        }
      }

    private transmitConsole() {
        const originalConsole = {
            log: console.log,
            error: console.error,
            warn: console.warn,
            info: console.info,
            debug: console.debug,
        };

        // 通用日志处理函数
        const createHandler = (type: string) => (...args: any[]) => {
            originalConsole[type].apply(console, args);  // 保持原始控制台输出
            if (this.socket.readyState != WebSocket.OPEN) {
                return;
            }
            // 将参数转换为字符串并用空格连接
            const message = args.map(arg => {
                try {
                    return typeof arg === 'object'
                        ? JSON.stringify(arg, null, 0)  // 紧凑模式
                        : String(arg);
                } catch {
                    return '[Circular]';
                }
            }).join(' ');  // 用单个空格连接

            const msg = this.formatMessage("", {
                type: type,
                data: message
            });
            this.socket.send(msg);
        };

        // 重写所有控制台方法
        console.log = createHandler('log');
        console.error = createHandler('error');
        console.warn = createHandler('warn');
        console.info = createHandler('info');
        console.debug = createHandler('debug');
    }


    onDestroy() {
        this.cleanup();
    }


}


