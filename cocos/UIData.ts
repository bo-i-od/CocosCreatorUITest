import { _decorator, Camera, Component, Node, UITransform, Vec3, screen, Slider, ProgressBar, Label, EditBox, RichText, Toggle, Sprite } from 'cc';
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
            let text: string = "";
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
        const richText = node.getComponent(EditBox);
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

}


