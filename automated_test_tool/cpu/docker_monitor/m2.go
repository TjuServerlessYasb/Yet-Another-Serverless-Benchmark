package main

import (
	"docker_monitor/util"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

var containerNames []string

func getCPUuasge(file *os.File, wg *sync.WaitGroup) {
	sum := 0.0
	var cpuList []string

	var wgson sync.WaitGroup
	wgson.Add(len(containerNames))
	for _, container := range containerNames {
		go func(sss string) {
			cmd := fmt.Sprintf("docker stats %s  --no-stream | awk 'NR==2' | awk '{print $3}'", sss)
			result, err := util.ExecCmd(cmd)
			if err != nil {
				fmt.Printf("%v", err)
				return
			}
			cpuList = append(cpuList, result)
			wgson.Done()
		}(container)
	}

	wgson.Wait()
	//fmt.Println(cpuList)
	for _, cpu := range cpuList {
		number := strings.Split(cpu, "%")
		float, err := strconv.ParseFloat(number[0], 64)
		if err != nil {
			fmt.Printf("%v", err)
			return
		}
		sum += float

	}
	file.WriteString(fmt.Sprintf("%v ", sum))
	wg.Done()
}

func main() {
	var functionName []string
	var duration int

	for idx, args := range os.Args {
		if idx == 0 {
			continue
		} else if idx == 1 {
			fmt.Println("测试时间", args)
			atoi, err := strconv.Atoi(args)
			if err != nil {
				fmt.Println("测试时间错误")
			} else {
				duration = atoi
			}
		} else {
			fmt.Println("函数名", args)
			functionName = append(functionName, args)
		}
	}

	var wg sync.WaitGroup

	wg.Add(duration * 10)

	for _, s := range functionName {
		//openfaas：
		cmd := fmt.Sprintf("docker ps | grep k8s_%s_ | awk '{print $NF}'", s)
		//ray：
		//cmd := fmt.Sprintf("docker ps | grep k8s_ray | awk '{print $NF}'", s)
		containerNamestemp, err := util.ExecCmd(cmd)
		if err != nil {
			fmt.Printf("%v", err)
			return
		}
		splits := strings.Split(containerNamestemp, "\n")
		//if len(splits) != 2 {
		//	fmt.Println("该函数名下不止一个实例")
		//	return
		//}
		splits = splits[:len(splits)-1]
		//fmt.Println(splits)
		//fmt.Println(len(splits))

		containerNames = append(containerNames, splits...)
	}

	for i := 0; i < len(containerNames); i++ {
		fmt.Println(containerNames[i])
	}

	timeNow := time.Now().Format("06_01_02_15_04_05")
	filename := fmt.Sprintf("%s_%s", functionName[0], timeNow)

	file, err := os.Create(filename)
	if err != nil {
		fmt.Printf("%v", err)
		return
	}
	defer file.Close()

	for i := 0; i < 10*duration; i++ {

		go getCPUuasge(file, &wg)
		time.Sleep(100 * time.Millisecond)
	}
	wg.Wait()

}
