import { _decorator, Camera, Component, Node, UITransform, Vec3, screen, Slider, ProgressBar, Label, EditBox, RichText, Toggle, Sprite, director, Director} from 'cc';
const { ccclass, property } = _decorator;

@ccclass('UIData')
export class UIData {
    public static getPositionArray(nodeArray: Node[],  uiCamer: Camera){
        let positionArray: number[][] = [];
        let cur: number = 0;
        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            const screenPos = new Vec3();
            const worldPos = node.getWorldPosition();
            uiCamer.worldToScreen(worldPos, screenPos);
            let screenVecNormalization: number[] = [0, 0];
            screenVecNormalization[0] = screenPos.x / screen.resolution.width;
            screenVecNormalization[1] = 1 - screenPos.y / screen.resolution.height;
            positionArray.push(screenVecNormalization);
            cur += 1;
        }
        return positionArray;
    }

    public static getSizeArray(nodeArray: Node[]){
        let sizeArray: number[][] = [];
        let cur: number = 0;
        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            const size = node.getComponent(UITransform).contentSize;
            let sizeNormalization: number[] = [0, 0];
            sizeNormalization[0] = size.width / screen.resolution.width;
            sizeNormalization[1] = size.height / screen.resolution.height;
            sizeArray.push(sizeNormalization);
            cur += 1;
        }
        return sizeArray;
    }

    public static correctPosition(positionArray: number[][], sizeArray: number[][], anchorPoint: number[]){
        let correctedPositionArray: number[][] = [];
        const biasX = 0.5 - anchorPoint[0];
        const biasY = 0.5 - anchorPoint[1];
        let cur: number = 0;
        while(cur < positionArray.length){
            correctedPositionArray.push([positionArray[cur][0] + sizeArray[cur][0] * biasX, positionArray[cur][1] += sizeArray[cur][1] * biasY]);
            cur += 1;
        }
        return correctedPositionArray;
    }


    public static getProgressArray(nodeArray: Node[]){
        let progressArray: number[] = [];
        let cur: number = 0;
        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            let progress: number = 0;
            const componentProgress = this.getComponentProgress(node);
            if(componentProgress){
                progress = componentProgress.progress;
            }
            progressArray.push(progress);
            cur += 1;
        }
        return progressArray;
    }

    public static getTextArray(nodeArray: Node[]){
        let textArray: string[] = [];
        let cur: number = 0;
        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            let text: string = "";
            const componentText = this.getComponentText(node);
            if(componentText){
                text = componentText.string;
            }
            textArray.push(text);
            cur += 1;
        }
        return textArray;
    }

    public static setTextArray(nodeArray: Node[], text: string){
        let cur: number = 0;
        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            const componentText = this.getComponentText(node);
            if(componentText){
                componentText.string = text;
            }
            cur += 1;
        }
    }

    public static getSpriteNameArray(nodeArray: Node[]){
        let spriteNameArray: string[] = [];
        let cur: number = 0;
        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            let sprite: string = node.getComponent(Sprite).spriteFrame.name;
            spriteNameArray.push(sprite);
            cur += 1;
        }
        return spriteNameArray;
    }

    public static getComponentProgress(node: Node){
        const slider = node.getComponent(Slider);
        if(slider){
            return slider;
        }
        const progressBar = node.getComponent(ProgressBar);
        if(progressBar){
            return progressBar;
        }
        return null;
    }

    public static getComponentText(node: Node){
        const label = node.getComponent(Label);
        if(label){
            return label;
        }
        const editBox = node.getComponent(EditBox);
        if(editBox){
            return editBox;
        }
        const richText = node.getComponent(RichText);
        if(richText){
            return richText;
        }
        return null;
    }

    public static getToggleIsCheckedArray(nodeArray: Node[]){
        let toggleIsCheckedArray: boolean[] = [];
        let cur: number = 0;
        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            let toggleIsChecked: boolean = node.getComponent(Toggle).isChecked;
            toggleIsCheckedArray.push(toggleIsChecked);
            cur += 1;
        }
        return toggleIsCheckedArray;
    }

    public static getNameArray(nodeArray: Node[]){
        let nameArray: string[] = [];
        let cur: number = 0;

        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            nameArray.push(node.name);
            cur += 1;
        }
        return nameArray;
    }

    
    public static getIDArray(nodeArray: Node[], idToNode: Map<string, Node>){
        let idArray: string[] = [];
        let cur: number = 0;
        while(cur < nodeArray.length){
            const node: Node = nodeArray[cur];
            idToNode.set(node.uuid, node);
            idArray.push(node.uuid);
            cur += 1;
        }
        return idArray;
    }

    public static async screenShot(x, y, width, height): Promise<[string, string]> {

        return new Promise((resolve, reject) => {
            // 确保在下一帧渲染后捕获
            director.once(Director.EVENT_AFTER_DRAW, () => {
                try {
                    const canvas = document.getElementById("GameCanvas") as HTMLCanvasElement;
                    
                    // 验证canvas有效性
                    if (!canvas || canvas.width === 0 || canvas.height === 0) {
                        throw new Error("Canvas not initialized");
                    }
                    // 坐标系转换：将中心点转换为左上角起点
                    let startX = x - width / 2;
                    let startY = y - height / 2;
                    
                    // 边界处理
                    startX = Math.max(0, Math.min(startX, canvas.width - 1));
                    startY = Math.max(0, Math.min(startY, canvas.height - 1));
                    
                    // 计算实际截取区域
                    const endX = Math.min(startX + width, canvas.width);
                    const endY = Math.min(startY + height, canvas.height);
                    const actualWidth = endX - startX;
                    const actualHeight = endY - startY;

                    // 创建临时Canvas
                    const tempCanvas = document.createElement('canvas');
                    tempCanvas.width = actualWidth;
                    tempCanvas.height = actualHeight;
                    const ctx = tempCanvas.getContext('2d')!;

                    // 九参数绘制解决边界溢出问题
                    ctx.drawImage(
                        canvas,
                        startX, startY,        // 源起点
                        actualWidth, actualHeight,  // 源尺寸
                        0, 0,                  // 目标起点
                        actualWidth, actualHeight  // 目标尺寸
                    );

    
                    // 必须配置preserveDrawingBuffer（在引擎初始化时设置）
                    const dataURL = tempCanvas.toDataURL('image/jpeg');
                    
                    // 提取base64数据
                    const base64Data = dataURL.split(',')[1];
                    
                    resolve([base64Data, 'jpg']);
                } catch (e) {
                    reject(["", "jpg"]);
                }
            });
    
            // 强制触发渲染更新
            director.getScene().renderScene.update(0);
        });
    }





}


