import { _decorator, Component, Node, log, screen } from 'cc';
const { ccclass, property } = _decorator;

@ccclass
export default class WSClient extends Component {
    private socket: WebSocket = null;
    private reconnectTimer: number = 0;
    private baseDelay = 1000;
    private rpcHandlers: { [key: string]: (params: any) => string } = {}; // RPC 方法注册表

    // 注册 RPC 方法
    registerRpcHandler(methodName: string, callback: (params: any) => string) {
        this.rpcHandlers[methodName] = callback;
    }


    onLoad() {
        this.registerRpcHandler("getScreenSize", this.getScreenSize.bind(this))
        this.startConnection();
        
    }

    // 获取分辨率
    private getScreenSize(params: {}) {
        return JSON.stringify(screen.resolution);
        // 这里添加实际的血量更新逻辑
    }

    startConnection() {
        this.cleanup();
        this.socket = new WebSocket("ws://localhost:5101");

        this.socket.onopen = () => {
            // this.scheduleHeartbeat();
            // this.socket.send("<----TypeScript->Python---->已连接");
        };

        this.socket.onmessage = (msg) => {
            let response = this.handleMessage(msg);
            this.socket.send(response);
        };

        this.socket.onclose = (ev) => {
            log(`连接关闭: ${ev.reason}`);
            this.handleReconnect();
        };

        this.socket.onerror = (err) => {
            log("WebSocket 连接失败，正在重试……");
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
            log(err);
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
      

    onDestroy() {
        this.cleanup();
    }


}


