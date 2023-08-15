package util

import (
	"os/exec"
)

func ExecCmd(cmd string) (string,error) {
	output, err := exec.Command("bash", "-c", cmd).Output()
	result := string(output)
	return result,err
}
