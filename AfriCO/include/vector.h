#ifndef VECTOR_HPP
#define VECTOR_HPP

#include <stdio.h>

// A linked list node 
template <typename T> 
class Node
{
public:
    T data;
    Node* next;
};

template <typename R>
class Vector: Node<R> {
private:
    Node<R>* head = nullptr;
    unsigned long l = 0;
public:
    Vector(){}
    ~Vector(){}
    /* Given a reference (pointer to pointer)
       to the head of a list and an int, inserts
       a new node on the front of the list. */
    void push(/*Node** head_ref*/ R new_data)
    {
        // 1. Allocate node  
        Node<R>* new_node = new Node<R>();

        // 2. Put in the data  
        new_node->data = new_data;

        // 3. Make next of new node as head 
        new_node->next = head;

        // 4. Move the head to point to the  
        //    new node  
        head = new_node;
        l += 1;
    }

    /* Given a node prev_node, insert a new
       node after the given prev_node */
    void insertAfter(/*Node* prev_node,*/ R new_data)
    {
        /* 1. Check if the given prev_node
              is NULL */
        if (head->next == NULL)
        {
            //cout << "the given previous node cannot be NULL";
            return;
        }

        // 2. Allocate new node  
        Node<R>* new_node = new Node<R>();

        // 3. Put in the data  
        new_node->data = new_data;

        // 4. Make next of new node as next  
        //    of prev_node  
        new_node->next = (head->next)->next;

        // 5. Move the next of prev_node  
        //    as new_node  
        (head->next)->next = new_node;
        l += 1;
    }

    /* Given a reference (pointer to pointer)
       to the head of a list and an int,
       appends a new node at the end */
    void append(/*Node** head_ref,*/ R new_data)
    {
        // 1. Allocate node  
        Node<R>* new_node = new Node<R>();

        // Used in step 5 
        Node<R>* last = head;

        // 2. Put in the data  
        new_node->data = new_data;

        /* 3. This new node is going to be
              the last node, so make next of
              it as NULL */
        new_node->next = NULL;

        /* 4. If the Linked List is empty,
        then make the new node as head */
        if (head == NULL)
        {
            head = new_node;
            l += 1;
            return;
        }

        // 5. Else traverse till the 
        //    last node  
        while (last->next != NULL)
            last = last->next;

        // 6. Change the next of last node  
        last->next = new_node;
        l += 1;
        return;
    }

    // This function prints contents of 
    // linked list starting from head  
    void printList(/*Node* node*/)
    {
        while (head != NULL)
        {
            //cout << " " << head->data;
            head = head->next;
        }
    }

    R pop() {
        
        if (head != NULL){
            Node<R>* tmp = head->next;
            R data = head->data;
            delete head;
            head = tmp;
            l -= 1;
            return data;
        }
        return (R)'\0';
    }

    unsigned long lenght() {
        return l;
    }

    R at(int index) {
        Node<R>* temp = head;
        int i = 0;
        if(temp != NULL)
        {
            while (temp != NULL && i<index) {
                temp = temp->next;
                i++;
            }
        }
        else {
            return NULL;
        }
        return temp->data;
    }
};

#endif