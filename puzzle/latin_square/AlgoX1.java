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
    private final int maxP; //max possibilities
    private final int maxC; //max constraints
    private boolean[] satisfiedC;
    private NODE root;
    private NODE[] cols;
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
    public AlgoX(LinkedList<DATA>[] list, int p, int c)
    {
        
        maxP = p;
        maxC = c;
        satisfiedC = new boolean[maxC+1];

        // create a root
        root = new NODE(0, 0);
        cols = new NODE[maxC+1];
       
        NODE prev = root;
        //create a doubly linked list of the cols, with root at the head
        for (int i = 1; i <= maxC; i++) {
            cols[i] = new NODE(0, i);
            insertLeft(root, cols[i]);
            satisfiedC[i] = false;
        }

        // Create a doubly linked list of each column elements
        // Create a doubly linked list of each row elements
        for (int i = 1; i <= maxP; i++) {
            boolean first = true;
            NODE l = null;
            for (DATA d:list[i]) {
                NODE nd = new NODE(d.r, d.c, d.v);

                insertTop(cols[d.c], nd);
                cols[d.c].count += 1;
                if (!first)                             //insert into row
                    insertLeft(l, nd);
                else 
                    first = false;

                l = nd;
            }
        }
    }

    // if minIndex == 0 , solved
    //             == -1, cannot be solved
    //  otherwise carry on with work
    public int minColumn(int l)
    {
        int min = maxP;
        int minIndex = 0;
        for (int i = 1; i <= maxC; i++) {
            if (!satisfiedC[i]) {
                int cnt = cols[i].count;
                if (cnt == 0)
                    return -1;
                if (cnt < min) {
                    min = cnt;
                    minIndex = i;
                }
            }
        }
        return minIndex;
    }


    public int minColumn()
    {
        int min = maxP;
        int minIndex = 0;
        for (NODE c = root.right; c != root; c = c.right) {
            if (!satisfiedC[c.col]) {
                int cnt = c.count;
                if (cnt == 0)
                    return -1;
                if (cnt < min) {
                    min = cnt;
                    minIndex = c.col;
                }
            }
        }
        return minIndex;
    }


    public boolean solved()
    {
        return (root == root.right);
    }


    public void print()
    {
        NODE r, c;
        for (r = root.right; r != root; r = r.right) {
            StdOut.println("===============================");
            r.print();
            StdOut.println("---------------");
            for (c = r.bottom; c != r; c = c.bottom) 
                c.print();
        }
    }

    public void detachNode(NODE h)
    {
       //disconnect from column
        NODE t, b;

        t = h.top;
        b = h.bottom;

        t.bottom = h.bottom;
        b.top    = h.top;
        cols[h.col].count -= 1;
    }


    public void attachNode(NODE h)
    {
        NODE t, b;
        t = h.top;
        b = h.bottom;

        t.bottom = h;
        b.top    = h;
        
        cols[h.col].count += 1;

    }

    public void detachRow(NODE h)
    {
        NODE p;
        //column node just return
        if (h.value == 0)
            return;
         

        //StdOut.println("Before Detaching Row  = " + h.row);
        //print();
        for (p = h.right; p != h; p = p.right) {
//            StdOut.print("Detaching node  = ");
//            p.print();
//            StdIn.readInt();
            detachNode(p);
//            print();
        }
//        StdOut.print("Detaching node  = ");
//        p.print();
        detachNode(p);
        StdOut.println("After Detaching Row  = " + h.row);
        //print();
    }

    public void attachRow(NODE h)
    {
        NODE p;
        if (h.value == 0)
            return;
        //StdOut.println("Before attaching row node  = " + h.row);
        //print();
        for (p = h.right; p != h; p = p.right) {
         //   StdOut.println("Attaching Row = ");
         //   p.print();
            attachNode(p);
         //   p.print();
        }
        //StdOut.println("Attaching Row = ");
        //p.print();
        attachNode(p);
        //StdOut.println("Before attaching row node  = " + h.row);
        //p.print();
    }

    public void attachCol(NODE c)
    {
        NODE l, r;

        l = c.left;
        r = c.right;
        l.right = c;
        r.left  = c;
    }


    public void detachCol(NODE c)
    {
        NODE l, r;

        l = c.left;
        r = c.right;
        l.right = r;
        r.left  = l;
        StdOut.println(">>>>>>>>>>>>>>>>>>>Detaching column = " + c.col);
//        print();
    }

    public void printSolution(Queue<Integer> q)
    {
        StdOut.println("found solution");
        for (int i:q) 
            StdOut.print(i + " ");

        StdOut.println();
    }


    public void processColRow(NODE h, Stack<NODE> st)
    {
        NODE p;
        for (p = h.bottom; p != h; p = p.bottom) {
            StdOut.println(">>>>>>>>>>>>>>>>>>Processing Row, Col = " + p.row + " " + p.col);
            detachRow(p);
            st.push(p);
        }
        st.push(cols[h.col]);
        detachCol(cols[h.col]);
    }

    public void processRow(NODE h, Stack<NODE> st)
    {
        //print(); 
        NODE p;
        for (p = h; p != h.left; p = p.right) {
            satisfiedC[p.col] = true;
            processColRow(p, st);
        }
        processColRow(p, st);
        st.push(h);
        detachRow(h);
        StdOut.println(">>>>>>>>>>>>>>>>>Finished Processing Row = " + h.row);
        print(); 
    }
   

    public void restore(Stack<NODE> st)
    {
        NODE h;
        while (!st.isEmpty())  {
            h = st.pop();
            if (h.value == 0)
                attachCol(h);
            else
                attachRow(h); 
            satisfiedC[h.col] = false;
        }
    }

    public void solve(Queue<Integer> q)
    {
        int mc = minColumn();
        StdOut.println("min column = >>>>>>>>>>>>>>>>>>>>>>>" + mc);
        if (mc == -1) {
            StdOut.println("No solution possible returning  **************************");
            return;
        }

        if (mc == 0) {
            printSolution(q);
            return;
        }

        assert(cols[mc].count > 0); 

        for (NODE h = cols[mc].bottom; h != cols[mc]; h = h.bottom) {
            if (h.row == 0)
                continue;
            StdIn.readInt();
            Stack<NODE> st = new Stack<>();
            StdOut.println("Selected row for processing = " + h.row);
            q.enqueue(h.row);
            processRow(h, st);
         //   print();
            solve(q);
            restore(st);
            StdOut.println(">>>>>>>>>>>>>>>>>>>>>>>>>>>>After restoring");
        //    print();
            q.dequeue();
            assert(st.isEmpty() == true);
        }
    }

    public Queue<Integer> solve()
    {
        Queue<Integer> q = new Queue<>();
        solve(q);
        return q;
	}

    public static void main(String[] args)
    {
        In in = new In(args[0]);
        String[] q = in.readLine().split("\\s+"); //StdIn.readLine().split("\\s+");
        int N = Integer.parseInt(q[0]);
        int M = Integer.parseInt(q[1]);
        LinkedList<DATA>[] list = new LinkedList[N+1];
        
        for (int i = 1; i <= N; i++) {
            list[i] = new LinkedList<DATA>();
            for (String s:in.readLine().split("\\s+")) { //StdIn.readLine().split("\\s+")) {
                list[i].addFirst(new DATA(i, Integer.parseInt(s), 1));
            }
        }
        AlgoX al = new AlgoX(list, N, M);
        al.solve();
    }
}
