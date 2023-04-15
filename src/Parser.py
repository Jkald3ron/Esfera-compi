import ply.yacc as yacc
import os
import codecs
import re
from Lexer import tokens
#EV3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import random

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('right', 'CASE', 'WHEN')
)

run_flag = True
pars = []
errors = []
names = {}
procs = {}

#Ev3 initializing
ev3 = EV3Brick()
#Motors initializing 
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
#Motor driver initializing
carBall = DriveBase(leftMotor, rightMotor, wheel_diameter = 55.5, axle_track = 104)

def p_symbols(p):
    'symbol : Body'
    p[0] = p[1]

start = 'Body'
def stop():
    carBall.stop()
    leftMotor.brake()
    rightMotor.brake()
    carBall.settings(straight_speed=3000,straight_acceleration=1500)

def p_statement_proc(p):
    'statement : PROC NAME "(" expression ")"'
    if len(p[2])>1 and len(p[2])<10 :
        procs[p[2]] = p[4]
    else:
        p[0]="Los procesos deben constar de minimo 3 caracteres y maximo 10 \ncontando con el @"

def p_statement_comment(p):
    'statement : COMMENT '

def p_statement_printline(p):
    'statement : PRINTLINE'

def p_statement_expr(p):
    '''
    statement : expression
              | expression statement
              |
    '''
    if len(p)==2:
        p[0]=(p[1])
    if len(p)==3:
        p[0]=(p[1],p[2])

def p_statement_print(p):
    '''
    statement : PRINT PRINTLINE
    '''
    p[0]=p[2]

def p_statement_case(p):
    '''statement : CASE WHEN expression statementt'''

    if p[3]:
        print('Esto es para separar')
        print(p[5])
        p[0] = p[5]

def p_statement_then(p):
    """ statementt : THEN statement """
    if p[-1]:
        print("ass")
        p[0] = p[2]
    else:
        a = p[2]
        if isinstance(a, list):
            b = a[0]
            c = a[1]
            if isinstance(c,int):
                names[b] = names[b] - c
            else:
                names.pop(b)
        else:
            print("aaa")
        print(names)

def p_statement_cases(p):
    """ statement : CASE expression """
    p[1] = p[2]
    p[0] = p[2]

def p_statement_when(p):
    """statement : statement WHEN expression statement"""

    if p[1] == p[3]:
        print("vamos bien")
        print(p[5])
        p[0] = p[5]
    else:
        p[0] = p[1]
        print("no entro")

def p_statement_else(p):
    '''statement : ELSE statement'''

    print(p[1])
    p[0] = p[1]
def p_statement_aleatorio(p):
    '''
    statement : ALEATORIO LPAREN RPAREN
    '''
    i = 10
    while i>0:
        a = random.randint(1, 8)
        
        if a == 1:
            carBall.straight(-200)
            stop()
        elif a == 2:
            carBall.straight(200)
            stop()
        elif a == 3:
            carBall.turn(45)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(-45)
            stop()
        elif a == 4:
            carBall.turn(-45)
            stop()
            carBall.straight(-200)
            stop()
            carBall.turn(45)
            stop()

        elif a == 5:
            carBall.turn(90)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(-90)
            stop()
        elif a == 6:
            carBall.turn(-90)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(90)
            stop()
        elif a == 7:
            carBall.turn(-45)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(45)
            stop()
        elif a == 8:
            carBall.turn(45)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(-45)
            stop()

def p_statement_horn(p):
    '''
    statement : HORN LPAREN RPAREN
    '''
    ev3.speaker.beep()


def p_statement_mover(p):
    '''
    statement : MOVER LPAREN MOVIMIENTO RPAREN SEMICOLON
    '''
    if p[3].value == 'ATR':
        print("La esfera va a moverse hacia atras")
        p[0]="La esfera va a moverse hacia atras"
        carBall.straight(-200)
        stop()
    
    elif p[3].value == 'ADL':
        print("La esfera va a moverse hacia delante")
        p[0]="La esfera va a moverse hacia delante"
        carBall.straight(200)
        stop()
    
    elif p[3].value == 'ADE':
        print("La esfera va a moverse hacia atras a la derecha")
        p[0]="La esfera va a moverse hacia atras a la derecha"
        carBall.turn(45)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(-45)
        stop()
    
    elif str(p[3]) == 'AIZ':
        print("La esfera va a moverse hacia atras a la izquierda")
        p[0]="La esfera va a moverse hacia atras a la izquierda"
        carBall.turn(-45)
        stop()
        carBall.straight(-200)
        stop()
        carBall.turn(45)
        stop()
    
    elif str(p[3]) == 'IZQ':
        print("La esfera va a moverse hacia la izquierda")
        p[0]="La esfera va a moverse hacia la izquierda"
        carBall.turn(90)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(-90)
        stop()

    elif str(p[3]) == 'DER':
        print("La esfera va a moverse hacia la derecha")
        p[0]="La esfera va a moverse hacia la derecha"
        carBall.turn(-90)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(90)
        stop()

    elif str(p[3]) == 'DDE':
        print("La esfera va a moverse hacia delante a la derecha")
        p[0]="La esfera va a moverse hacia delante a la derecha"
        carBall.turn(-45)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(45)
        stop()
    
    elif str(p[3]) == 'DIZ':
        print("La esfera va a moverse hacia delante a la izquierda")
        p[0]="La esfera va a moverse hacia delante a la izquierda"
        carBall.turn(45)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(-45)
        stop()

    elif str(p[3]) == 'SPINL':
        print("La esfera va a dar varias vueltas hacia la izquierda")
        p[0]="La esfera va a dar varias vueltas hacia la izquierda"
        carBall.turn(-1080)
        stop()

    elif str(p[3]) == 'SPINR':
        print("La esfera va a dar varias vueltas hacia la derecha")
        p[0]="La esfera va a dar varias vueltas hacia la derecha"
        carBall.turn(1080)
        stop()


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_relation_GT(p):
    """ relation : GT """
    p[0] = '>'

def p_relation_LT(p):
    """ relation : LT """
    p[0] = '<'

def p_relation_GTE(p):
    """ relation : GTE """
    p[0] = '>='

def p_relation_LTE(p):
    """ relation : LTE """
    p[0] = '<='

def p_relation_NE(p):
    """ relation : NE """
    p[0] = '<>'

def p_relation_EQUAL(p):
    ''' relation : EQUAL '''
    p[0] = '=='

def p_expression_compr(p):
    '''expression : expression relation expression'''

    if isinstance(p[1], int) and isinstance(p[3], int):
        if p[2] == '<':
            print(p[1] < p[3])
            p[0] = p[1] < p[3]
        elif p[2] == '>':
            print(p[1] > p[3])
            p[0] = p[1] > p[3]
        elif p[2] == '<=':
            print(p[1] <= p[3])
            p[0] = p[1] <= p[3]
        elif p[2] == '>=':
            print(p[1] >= p[3])
            p[0] = p[1] >= p[3]
        elif p[2] == '<>':
            print(p[1] != p[3])
            p[0] = p[1] != p[3]
        elif p[2] == '==':
            print(p[1] == p[3])
            p[0] = p[1] == p[3]
        else:
            print("no sirve")
    else:
        p[0]="Compara valores no validos"

def p_expression_istrue(p):
    '''expression : ISTRUE LPAREN expression RPAREN SEMICOLON '''

    if isinstance([3], bool):
        if p[3] == True:
            p[0] = True
            print("True")
        else:
            p[0] = False
            print("False")
    else:
        p[0]="IsTrue con formatos no validos "
def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : LPAREN expression RPAREN "
    p[0] = p[2]

def p_expression_integer(p):
    "expression : INTEGER"
    p[0] = p[1]

def p_expression_bool(p):
    "expression : BOOL"
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]][1]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_expression_def(p):
    '''expression : DEF LPAREN NAME COMMA TYPE COMMA INTEGER RPAREN SEMICOLON
                  | DEF LPAREN NAME COMMA TYPE COMMA BOOL RPAREN SEMICOLON
                  | DEF LPAREN NAME COMMA TYPE RPAREN SEMICOLON '''
    if len(p[3])>1 and len(p[3])<=10 :
        if p[6]== ',':
            if (p[5]=='integer'):
                if isinstance(p[7],int):
                    names[p[3]] = [p[5],p[7]]
                else:
                    print ("Error, tipo de la variable no coincide con el valor dado")
            elif (p[5]=='boolean'):
                if isinstance(p[7],bool):
                    names[p[3]] = [p[5],p[7]]
                else:
                    print ("Error, tipo de la variable no coincide con el valor dado")
        elif p[6]==')':
            names[p[3]] = [p[5],None]

def p_expression_change(p):
    'expression : NAME "(" expression ")"'
    if names[p[1]][0]=="integer":
        if names[p[1]]!=None and isinstance(names[p[1]][1], int)^isinstance(p[3],bool):
            names[p[1]][1]=p[3]
    elif names[p[1]][0]=="boolean":
        if names[p[1]]!=None and (names[p[1]][0]=="boolean") ^ isinstance(p[3],int) :
            names[p[1]][1]=p[3]
    else:
        print("El valor asignado a la variabl debe ser del mismo tipo")

def p_expression_not(p):
    'expression : NOT "(" NAME ")"'
    temp=names[p[3]][1]
    if temp:
        names[p[3]][1]=False
    else:
        names[p[3]][1]=True


def p_expression_math(p):
    'expression : ALTER "(" NAME "," expression ")"'
    if isinstance(p[5], int) and isinstance(names[p[3]][1], int):

        names[p[3]][1] = names[p[3]][1] + p[5]
    else:
        print("La funcion alter solo cambia el valor de las variables númericas")

def p_expression_repeat(p):
    '''
    expression : REPEAT LPAREN expression SEMICOLON BREAK SEMICOLON RPAREN SEMICOLON
    '''
    p[0]=(p[1],p[3])

def p_expression_repeat_error(p):
    '''
    expression : REPEAT LPAREN expression SEMICOLON RPAREN SEMICOLON
    '''
    p[0]="Error expected break not found"

def p_expression_until(p):
    '''
    expression : UNTIL LPAREN expression RPAREN statement SEMICOLON
    '''
    p[0]=(p[1],p[3],p[5])

def p_expression_until_error(p):
    '''
    expression :  UNTIL LPAREN expression RPAREN
          |  UNTIL LPAREN expression RPAREN SEMICOLON
    '''
    p[0]="Error expected condition not found"

def p_statement_while(p):
    '''
    statement : WHILE LPAREN expression RPAREN LPAREN statement RPAREN SEMICOLON
    '''
    print(p[3])
    if p[3]==True:
        p[0]=(p[1],p[6])

def p_expression_Body(p):
    '''
    Body : expression statement expression
         | expression statement
         | statement expression
         | statement
         | statement statement
         | statement expression statement
         | expression expression
    '''

    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

def readFile(dir, run):
    if not run:
        run_flag = False
    fp = codecs.open(dir, "r", "utf-8")
    cadena = fp.read()
    parser = yacc.yacc()
    fp.close()
    par = parser.parse(cadena)
    pars.append(par)
    return pars

def clearpars():
    errors.clear()
    pars.clear()