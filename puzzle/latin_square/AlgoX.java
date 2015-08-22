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
    private NODE root;
    private static class DATA {
        private int r, c, v;
        public DATA(int r, int c, int v)
        {
            this.r = r;
            this.c = c;
            this.v = v;
        }
    }
    private static class NODE {
        private int row, col, value, count;
        private NODE left, right;
        private NODE top, bottom;
       
        public void init(int r, int c, int v)
        {
            row    = r;
            col    = c;
            value  = v;
            count  = 0;
            left   = this;
            right  = this;
            top    = this;
            bottom = this; 
        }

        public NODE(int r, int c)
        {
            init(r, c, 0);
        }
   
        public NODE(int r, int c, int v)
        {
            init(r, c, v);
        }
        public void print()
        {
            if (value == 0)
                StdOut.print("Col node:");
            else
                StdOut.print("Nor node:");

            StdOut.println("(" + row + "," + col + " = " + value + "," + count + ")");
        }

    }
    
    public void insertLeft(NODE h, NODE p)
    {
        NODE last = h.left;
       
        last.right = p;
        p.left     = last;

        h.left     = p;
        p.right    = h;
    }


    public void insertTop(NODE h, NODE p)
    {
        NODE last = h.top;
        
        last.bottom = p;
        p.top       = last;

        h.top       = p;
        p.bottom    = h;
    }

    //linked list of constrains, and the total number of constraints
    public AlgoX(LinkedList<DATA>[] list, int N)
    {
        root = new NODE(0, 0);
        NODE[] cols = new NODE[N];
       
        NODE prev = root;
        //Create a doubly linked list of the root + cols
        for (int i = 1; i <=N; i++) {
            cols[i-1] = new NODE(0, i);
            insertLeft(root, cols[i-1]);
        }

        // Create a doubly linked list of each column elements
        // Create a doubly linked list of each row elements
        for (int i = 0; i < N; i++) {
            boolean first = true;
            NODE l = null;
            for (DATA d:list[i]) {
                NODE nd = new NODE(d.r, d.c, d.v);

                insertTop(cols[d.c-1], nd);
                cols[d.c-1].count += 1;
                if (!first)                             //insert into row
                    insertLeft(l, nd);
                else 
                    first = false;

                l = nd;
            }
        }
    }

    public void print()
    {
        NODE r, c;
        for (r = root.right; r != root; r = r.right) {
            StdOut.println("======================");
            r.print();
            for (c = r.bottom; c != r; c = c.bottom) 
                c.print();
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
                list[i].add(new DATA(i+1, Integer.parseInt(s), 1));
            }
        }
        AlgoX al = new AlgoX(list, N);
        al.solve();
        al.print();
    }
}
