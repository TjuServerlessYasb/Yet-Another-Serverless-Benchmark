from ray import serve
from typing import List, Dict



@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class ArrangedProblemsService(object):
    # def __init__(self):
    def ArrangedProblems(self, body: Dict):
        print(123)
        try:

            event = body
            problems = event["problems"]
            answer = event["answer"]
            # Check the number of problems
            if len(problems) > 5:
                return "Error: Too many problems."

            first_operand = []
            second_operand = []
            operator = []

            for problem in problems:
                pieces = problem.split()
                first_operand.append(pieces[0])
                operator.append(pieces[1])
                second_operand.append(pieces[2])

            # Check for * or /
            if "*" in operator or "/" in operator:
                return "Error: Operator must be '+' or '-'."

            # Check the digits
            for i in range(len(first_operand)):
                if not (first_operand[i].isdigit() and second_operand[i].isdigit()):
                    return "Error: Numbers must only contain digits."

            # Check the length
            for i in range(len(first_operand)):
                if len(first_operand[i]) > 4 or len(second_operand[i]) > 4:
                    return "Error: Numbers cannot be more than four digits."

            first_line = []
            second_line = []
            third_line = []
            fourth_line = []

            for i in range(len(first_operand)):
                if len(first_operand[i]) > len(second_operand[i]):
                    first_line.append(" " * 2 + first_operand[i])
                else:
                    first_line.append(" " * (len(second_operand[i]) - len(first_operand[i]) + 2) + first_operand[i])

            for i in range(len(second_operand)):
                if len(second_operand[i]) > len(first_operand[i]):
                    second_line.append(operator[i] + " " + second_operand[i])
                else:
                    second_line.append(
                        operator[i] + " " * (len(first_operand[i]) - len(second_operand[i]) + 1) + second_operand[i])

            for i in range(len(first_operand)):
                third_line.append("-" * (max(len(first_operand[i]), len(second_operand[i])) + 2))

            if answer:
                for i in range(len(first_operand)):
                    if operator[i] == "+":
                        ans = str(int(first_operand[i]) + int(second_operand[i]))
                    else:
                        ans = str(int(first_operand[i]) - int(second_operand[i]))

                    if len(ans) > max(len(first_operand[i]), len(second_operand[i])):
                        fourth_line.append(" " + ans)
                    else:
                        fourth_line.append(
                            " " * (max(len(first_operand[i]), len(second_operand[i])) - len(ans) + 2) + ans)
                arranged_problems = "    ".join(first_line) + "\n" + "    ".join(second_line) + "\n" + "    ".join(
                    third_line) + "\n" + "    ".join(fourth_line)
            else:
                arranged_problems = "    ".join(first_line) + "\n" + "    ".join(second_line) + "\n" + "    ".join(
                    third_line)


        except Exception as e:
            print(e)
            print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
            print(e.__traceback__.tb_lineno)  # 发生异常所在的行数
        else:
            print("success")


        return arranged_problems
