/*
 * Basic structure where COL, E, ROOT are doubly linked list.
root-> COL1->COL2 -> COL3->....->COLN
       |     |       |            |
       v     V       V            v
      E11 -> E12 -> E13 -> ... ->E1N 
       |     |       |
       |     V       V
       |     E22 -> E23
       |     |
       V     v
       E31-> E32
 
       each COL also maintains the number of current elements


“Algorithm X”

We can find solution sets, if any exist, by a straightforward application of 
depth-first search with backtracking. In particular, we can incrementally build 
up a set of rows making up a solution as follows:

1.  Pick an unsatisfied constraint: that is, a column with no black cell 
    in any of the rows in the solution set. If there are no unsatisfied 
    constraints remaining, the solution set is complete: if all we wanted 
    was any solution, we’re done; if we want all solutions, then make note 
    of the solution we’ve got and then backtrack to the previous time we 
    chose a row and take the next choice instead.

2.  Pick a row that satisfies that constraint: that is, one with a black 
    cell in the chosen column. If there is no such row, then we’ve reached 
    a dead end and we must backtrack to the previous time we chose a row and 
    take the next choice instead.

3.  Add that row to the solution set.

4.  Delete all rows that satisfy any of the constraints satisfied by 
    the chosen row: that is, all rows that have a black cell in the same 
    column as a black cell in the chosen row.

5.  Return to step 1.



 */


import java.util.*;
public class AlgoX {
    NODE root;
    public static class DATA {
        int p;
        int v;
        public DATA(int p, int v)
        {
            this.p = p;
            this.v = v;
        }
    }
    private class NODE {
        NODE left, right;
        NODE top, bottom;
        int count, value;
       
        public void init(int v)
        {
            value  = v;
            count  = 0;
            left   = this;
            right  = this;
            top    = this;
            bottom = this; 
        }

        public NODE()
        {
            init(0);
        }
   
        public NODE(int v)
        {
            init(v);
        }

    }
    //linked list of constrains, and the total number of constraints
    public AlgoX(LinkedList<DATA>[] list, int N)
    {
        root = new NODE();
        NODE[] cols = new NODE[N];
       
        NODE prev = root;
        //Create a doubly linked list of the root + cols
        for (int i = 0; i < N; i++) {
            cols[i] = new NODE();
            cols[i].left  = prev;    cols[i].right  = root;
            prev = cols[i];
        }
        // Create a doubly linked list of each column elements
        // Create a doubly linked list of each row elements
        for (int i = 0; i < N; i++) {
            boolean first = true;
            NODE l, r;
            l = null;
            for (DATA d:list[i]) {
                NODE nd = new NODE(d.v);
                NODE c = cols[d.p];
                NODE t = c.top;
                t.bottom = nd; 
                c.top    = nd;
                nd.top     = t;
                nd.bottom  = c;
                    
                //insert into row
                if (!first) {
                    NODE right; 
                    r = l.right;
                    l.right = nd;
                    r.left = nd;
                    nd.left = l;
                    nd.right = r;
                    first = false;
                }
                l = nd;
            }
        }
    }
    public void print()
    {
        NODE n = root->right;
        while (n != root) {
            NODE f = n->
            for (i
        }
    }

    public Queue<Integer> solve()
    {
        Queue<Integer> q = new Queue<>();
        return q;
    }

    public static void main(String[] args)
    {
        String[] q = StdIn.readLine().split("\\s+");
        int N = Integer.parseInt(q[0]);
        LinkedList<DATA>[] list = new LinkedList[N];
        
        for (int i = 0; i < N; i++) {
            list[i] = new LinkedList<DATA>();
            for (String s:StdIn.readLine().split("\\s+")) {
                list[i].add(new DATA(Integer.parseInt(s), 1));
            }
            for (DATA d:list[i])
                StdOut.println(d.p + " " + d.v);
        }
        AlgoX al = new AlgoX(list, N);
        al.solve();
    }
}
