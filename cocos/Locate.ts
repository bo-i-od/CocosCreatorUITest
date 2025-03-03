import { _decorator, find, Node } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('Locate')
export class Locate {
    // 输入 定位信息
    // 输出 对应Node列表
    public static locateNodeArray(locator)
    {
        let nodeArray: Node[] = [];
        nodeArray = this.getChildNodeArray(nodeArray);
        let locatorArray: string[] = locator.split('>');
        // 查找起始节点
        let rootNode: Node = find(locatorArray[0]);
        
        if(rootNode == null)
        {
            return nodeArray;
        }
        nodeArray = this.getNodeArrayByChild(locatorArray, rootNode, nodeArray);
        return nodeArray;
    }

    // 输入Node列表
    // 输出子物体们的Node列表
    private static getChildNodeArray(nodeArray: Node[])
    {
        if (nodeArray.length == 0)
        {
            return nodeArray;
        }
        let nodeArrayNew:Node[] = [];
        let transformListCount:number = nodeArray.length;
        let cur:number = 0;
        while (cur < transformListCount)
        {
            nodeArrayNew = this.addChildren(nodeArray[cur], nodeArrayNew);
            cur += 1;
        }
        return nodeArrayNew;
    }

    // 根据locatorArray[]依次找节点列表
    private static getNodeArrayByChild(locatorArray: string[], rootNode: Node, nodeArray: Node[])
    {
        let index: number = 0;
        let locatorArrayLen: number = locatorArray.length;
        // 列表为空时添加第一个节点

        nodeArray.push(rootNode);
        if (locatorArrayLen > 0 && rootNode.name == locatorArray[0])
        {
            index += 1;
        }
        while (index < locatorArrayLen)
        {
            // 如果 locator 是空获得所有子物体Node
            if (locatorArray[index] == "")
            {
                nodeArray = this.getChildNodeArray(nodeArray);
                index += 1;
                continue;
            }
            // 获得该物体Node
            nodeArray = this.updateNodeArrayByChild(locatorArray[index], nodeArray);
            index += 1;
        }
        return nodeArray;
        // 直到找到最后
    }

    //输入 Node
    //返回 它们的孩子的Node列表
    private static addChildren(parent: Node, nodeArrayNew: Node[])
    {
        let childCount: number = parent.children.length;
        let childIndex: number = 0;
        while(childIndex < childCount)
        {
            let child:Node = parent.children[childIndex];
            childIndex += 1;
            //只添加激活了的
            if (!child.activeInHierarchy)
            {
                continue;
            }
            nodeArrayNew.push(child);
        }
        return nodeArrayNew;
    }

    // 根据locator在子物体中找到下一节点列表 
    private static updateNodeArrayByChild(locator: string, nodeArray: Node[])
    {
        let resList: Node[] = [];
        let nodeArrayCount: number = nodeArray.length;
        let cur: number = 0;
        while (cur < nodeArrayCount) {
            let childCount: number = nodeArray[cur].children.length;
            let i: number = 0;
            while(i < childCount)
            {
                let childNode: Node = nodeArray[cur].children[i];
                if (!childNode.activeInHierarchy)
                {
                    i += 1;
                    continue;
                }
                if(childNode.name != locator)
                {
                    i += 1;
                    continue;
                }
                resList.push(childNode);
                i += 1;
            }
            cur += 1;
        }
        return resList;
    }

    public static getNodeArrayByID(id: string, offspringPath: string, idToNode: Map<string, Node>)
    {
        let nodeArray: Node[] = [];
        let cur: number = 0;

        let targetNode: Node = this.getNodeByID(id, idToNode);
        if (targetNode == null)
        {
            return nodeArray;
        }
        nodeArray.push(targetNode);

        let locatorArray: string[] = offspringPath.split('>');
        // 没有locator就直接返回
        if(locatorArray.length == 1 && locatorArray[0] == "")
        {
            return nodeArray;
            //string[] result = new string[locatorArray.Length - 1];
            //Array.Copy(locatorArray, 1, result, 0, locatorArray.Length - 1);
            //locatorArray = result;
        }
        cur = 0;
        while (cur < locatorArray.length)
        {
            // 如果 locator 是空获得所有子物体Transform
            if (locatorArray[cur] == "")
            {
                nodeArray = this.getChildNodeArray(nodeArray);
                cur += 1;
                continue;
            }
            // 获得该物体Transform
            nodeArray = this.updateNodeArrayByChild(locatorArray[cur], nodeArray);
            cur += 1;
        }
        return nodeArray; 
    }

    public static getNodeByID(id: string, idToNode: Map<string, Node>)
    {
        if(!idToNode.has(id)){
            return null;
        }
        const node: Node = idToNode.get(id);
        if(!node.activeInHierarchy){
            return null;
        }
        return node;
        
    }

    public static getParentNodeArray(nodeArray: Node[])
    {
        if (nodeArray.length == 0)
        {
            return nodeArray;
        }
        let nodeArrayLength = nodeArray.length;
        let cur = 0;
        while (cur < nodeArrayLength)
        {
            nodeArray[cur] = nodeArray[cur].parent;
            cur += 1;
        }
        return nodeArray;
    }


}


